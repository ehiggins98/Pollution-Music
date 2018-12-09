import scraper
import time
from magenta.models.performance_rnn import performance_rnn_generate as generator
from multiprocessing import Process
from shutil import copyfile

root = '.'
bundle_file = root + '/multiconditioned_performance_with_dynamics.mag'
output_dir = root + '/tmp/performance_rnn/generated'

def generate_midi():
    _, histogram, notes_per_second, temperature = scraper.get_data()
    generator.init(bundle_file, 'multiconditioned_performance_with_dynamics', output_dir, 1, 12000, '', temperature, histogram, notes_per_second)
    with open('tmp.midi', 'wb+') as f:
        f.write(generator.run()[0])
    copyfile('tmp.midi', 'current.midi')

if __name__ == '__main__':
    generate_midi()