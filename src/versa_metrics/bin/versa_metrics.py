import os, json, re, yaml, argparse, time, random
import telnetlib, pexpect
from collections import defaultdict
from prometheus_client import start_http_server, Summary
from prometheus_client.core import Metric, REGISTRY

HOSTNAME = "localhost"
REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')


def get_config(config_file):
    '''Return configuration as yaml'''
    config_data = yaml.load_all(config_file)
    return config_data


def get_config_sections(config_data):
    config_sections = {}
    for each_section in config_data:
        if 'tmp_dir' in each_section:
            config_sections['tmp_dir'] = each_section['tmp_dir']
        if 'exclude_metrics' in each_section:
            config_sections['exclude_metrics'] = each_section['exclude_metrics']
        if 'log_dir' in each_section:
            config_sections['log_dir'] = each_section['log_dir']
        if 'debug' in each_section:
            config_sections['debug'] = each_section['debug']
        if 'cli_stats' in each_section:
            config_sections['cli_commands'] = each_section['cli_stats']
        if 'vsm_stats' in each_section:
            config_sections['vsm_commands'] = each_section['vsm_stats']
    return config_sections


def get_vsm_data(command):
    '''Get vsm metrics'''
    try:
        print "get_vsm_data return metrics %s" % (command)
        delimitter = ['Number of RX Poller Threads', 'Number of Worker Threads',
                      'Number of Control Threads', 'Number of Control Traffic Threads']
        tn = telnetlib.Telnet()
        port = 9001
        vnf_data = {}
        raw_dict = {}
        result = True
        linesout = list()
        tn.open(HOSTNAME, port)
        tn.read_until('vsm-vcsn0> ')
        tn.write(command.encode('ascii') + '\n')
        linesout.append(tn.read_until('vsm-vcsn0> ').replace('\r', ' '))
        result = linesout
        aggr_data = result[0].split("aggregated stats")[1]
        c_data = aggr_data.split("\n \n")
        for data in c_data:
            k = data.split('\n')
            for l in delimitter:
                for element in k:
                    if element.startswith(l):
                        k.remove(element)
                        key = l.split("Number of")[1].strip().replace(" ", "_").lower()
                        count = element.split(l)[1].strip().split()[0].split('[')[1].split(']')[0]
                        k.append("count : %s" % (count))
                        raw_dict[key] = k

        if raw_dict:
            for rkey, rval in raw_dict.items():
                for r in rval:
                    if re.search(':', r):
                        data = r.rsplit(':', 1)
                        key = 'vnf_' + rkey + '_' + data[0].strip().replace('-', "").replace("  ", "_").replace(" ",
                                                                                                                "_").lower()
                        value = data[1].replace(":", "").strip()
                        vnf_data[key] = value
            print "get_vsm_data return metrics %d" % (len(vnf_data))
            return vnf_data

    except Exception as e:
        print e.message
    finally:
        tn.close()


def get_versa_cli(commands):
    '''Get status from versa cli'''
    cli_metrics = {}
    for name, command in commands.items():
        random_text = str(random.random())
        output_file = "%s/%s.%s.json" % (tmp_dir, name, random_text)
        if os.path.isfile(output_file):
            os.unlink(output_file)
        command = command + " | save " + output_file
        print "Executing check_versa_cli %s" % (command)
        try:
            child = pexpect.spawn('/opt/versa/confd/bin/confd_cli -u admin')
            child.expect(".*-red> ")
            child.sendline(command)
            child.expect(".*-red> ")
            child.sendline('exit')
            child.close()
        except Exception, e:
            print "Import error, error : '%s'" % str(e)

        if os.path.isfile(output_file):
            with open(output_file) as json_data:
                data = json.load(json_data)
                if data:
                    os.unlink(output_file)
                    print "get_versa_cli return %d metrics" % (len(data))
                    cli_metrics[name] = data
    print '%s' % (cli_metrics)
    return cli_metrics


class DataPublisher(object):
    '''DataPublisher class'''

    def __init__(self, service='', exclude=list, cli_commands=dict, vsm_commands=dict):
        self.__all_metrics = defaultdict(list)
        self._service = service
        self._cli_stats = cli_commands
        self._vsm_stats = vsm_commands
        self._exclude = exclude
        self._labels = {}

    def _set_labels(self):
        '''Set labels'''
        self._labels.update({'service': self._service})

    def _filter_exclude(self, metrics):
        '''Exclude metrics'''
        return {k: v for k, v in metrics.items() if k not in self._exclude}

    @REQUEST_TIME.time()
    def _get_metrics(self):
        '''Get statistics from versa vnf'''
        self._all_metrics = defaultdict(list)
        self._labels = {}
        if self._vsm_stats:
            for name, command in self._vsm_stats.items():
                vsm_data = get_vsm_data(command)
                if vsm_data:
                    for key, value in vsm_data.items():
                        metrics_data = {}
                        metrics_data['value'] = value
                        self._all_metrics[key].append(metrics_data)

        if self._cli_stats:
            cli_metrics = get_versa_cli(self._cli_stats)
            stats_data = cli_metrics['log_collector_exporter']['data']
            if stats_data:
                log_op = stats_data['lced:log-collector-exporter']
                data = log_op['local']['collectors']['collector'][0]['statistics'][0]
                for key, value in data.items():
                    metrics_data = {}
                    metrics_data['value'] = value
                    self._all_metrics[key].append(metrics_data)

        # Return aggregated metrics
        if self._exclude and self._all_metrics:
            metrics = self._filter_exclude(self._all_metrics)
            print "aggregated metrics: %s" % (metrics)
            return metrics

    def collect(self):
        '''Yield collected statistics'''
        metrics = self._get_metrics()
        print "Collect function; number of metrics %d" % len(metrics)
        if metrics:
            for m, n in metrics.items():
                self._labels = {}
                s = m.replace("-", "_")
                metric = Metric(self._service + "_" + s, s, 'counter')
                for e in n:
                    if 'label' in e:
                        self._labels = e['label']
                        self._labels = {l_key.replace('-', '_'): l_val.replace('-', '_') for (l_key, l_val) in
                                        self._labels.items()}
                    value = e['value']
                    metric.add_sample(self._service + "_" + s, value=float(value), labels=self._labels)
                if metric.samples:
                    yield metric
                else:
                    pass


def main():
    '''
        Main Function
    '''
    global tmp_dir
    tmp_dir = "/tmp"

    try:
        parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        parser.add_argument('-c', '--config', help="Configuration file")
        parser.add_argument('-p', '--port', default='8889', help="Versa Exporter port")
    except KeyboardInterrupt:
        print "Ctrl + C to exiting....."

    args = parser.parse_args()
    if args:
        port = args.port
        config_file = args.config if args.config else '/opt/vnf_metrics/etc/vnf_config.yml'
    else:
        print "incorrect arguments passed....!!!!"

    config_file_obj = open(config_file, "r")
    config_data = get_config(config_file_obj)
    configuration_sections = get_config_sections(config_data)

    print "configuration_sections: ", configuration_sections

    try:
        REGISTRY.register(
            DataPublisher("vsg", configuration_sections['exclude_metrics'], configuration_sections['cli_commands'],
                          configuration_sections['vsm_commands']))
        start_http_server(int(port))
        while True: time.sleep(1)
    except KeyboardInterrupt:
        print("Interrupted")
        exit(0)


if __name__ == '__main__':
    main()