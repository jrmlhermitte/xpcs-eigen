import os
import yaml
import h5py
import numpy as np

HOMEDIR = os.path.expanduser("~/")
PROJDIR = HOMEDIR + "/research/projects/xpcs-aps-chx-project"
DATADIR = PROJDIR + "/sample_data/flow10crlT0_EGhtd_011_66"
filename = DATADIR + "/flow10crlT0_EGhtd_011_66_master.h5"

DATADIR = PROJDIR + "/storage/results"
filename = DATADIR + "/flow10crlT0_EGhtd_011_66_0001-10000.hdf"


type_map = [
    ('compression_mode', '/xpcs/compression', str),
    ('output_path', '/xpcs/output_data', str),
    ('dqmap', '/xpcs/dqmap', np.array),
    ('sqmap', '/xpcs/sqmap', np.array),
    ('xdim', '/measurement/instrument/detector/x_dimension', int),
    ('ydim', '/measurement/instrument/detector/y_dimension', int),
    ('frameStart', '/xpcs/data_begin', int),
    ('frameEnd', '/xpcs/data_end', int),
    ('frameStartTodo', '/xpcs/data_begin_todo', int),
    ('frameEndTodo', '/xpcs/data_end_todo', int),
    ('delays_per_level_', '/xpcs/delays_per_level', int),
    ('darkFrameStart', '/xpcs/dark_begin_todo', int),
    ('darkFrameEnd', '/xpcs/dark_end_todo', int),
    ('frame_stride_', '/xpcs/stride_frames', int),
    ('frame_average_', '/xpcs/avg_frames', float),
    ('m_detDpixX', '/measurement/instrument/detector/x_pixel_size', float),
    ('m_detDpixY', '/measurement/instrument/detector/y_pixel_size', float),
    ('m_detAdhupPhot', '/measurement/instrument/detector/adu_per_photon', float),
    ('m_detPreset', '/measurement/instrument/detector/exposure_time', float),
    ('m_detEfficiency', '/measurement/instrument/detector/efficiency', float),
    ('detDistance', '/measurement/instrument/detector/distance', float),
    ('fluxTransmitted',
     '/measurement/instrument/source_begin/beam_intensity_transmitted', float),
    ('thickness', '/measurement/sample/thickness', float),
    ('m_staticWindow', '/xpcs/static_mean_window_size', float),
    ('flatfield_enabled', '/xpcs/flatfield_enabled', str),
    ('flatfield', '/measurement/instrument/detector/flatfield', float),
    ('m_immFile', '/xpcs/input_file_local', str),
]


class Configuration:
    def __init__(self, filename):
        '''
            make configuration from an hdf5 data set
        '''
        # first just grab the data from hdf5
        # don't raise as some items may not be needed
        with h5py.File(filename) as f:
            # check if there is compression
            data_dict = dict()
            for key, val, dt in type_map:
                try:
                    data_dict[key] = dt(f[val].value)
                except KeyError:
                    data_dict[key] = None

        # validation step
        for key in ['dqmap', 'sqmap', 'xdim', 'ydim', 'frameStart',
                         'frameEnd', 'frameStartTodo', 'frameEndTodo',
                    'm_staticWindow',
                         'compression_mode']:
            if data_dict.get(key, None) is None:
                raise TypeError(f"{key} is not defined")

        # extraction step
        for key in ['dqmap', 'sqmap', 'xdim', 'ydim', 'frameStart',
                         'frameEnd', 'frameStartTodo', 'frameEndTodo',
                    'm_staticWindow',
                    ]:
            self.__dict__[key] = data_dict[key]
        # we now have the data dictionary, now create items
        self.compression = data_dict['compression_mode'].upper() == "ENABLED"

        self.m_totalStaticPartitions = 0;
        self.m_totalDynamicPartitions = 0;

        if data_dict['flatfield_enabled'].upper() == "ENABLED":
            self.flatfield = data_dict['flatfield']
        else:
            self.flatfield = np.zeros((self.xdim, self.ydim))

        self.buildQMap()

    def buildQMap(self):
        # TODO: understand the rest of his code later. I 
        # didn't understand yet
        self.m_validPixelMask = (self.dqmap > 0)*(self.sqmap > 0)
        self.m_totalDynamicPartitions = np.argmax(dqmap)
        self.m_totalStaticPartitions = np.argmax(sqmap)
        self.m_sbin = sqmap

config = Configuration(filename)
