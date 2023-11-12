from abc import ABC, abstractmethod # Used  to declare abstract class and pure virtual functions
import Modes
class BaseMode(ABC):
    def __init__(self, input_time_graph, output_time_graph, frequency_graph, input_spectro, output_spectro, slider1, slider2, slider3, slider4):
        self.time_graph = Modes.TimeGraph(input_time_graph, output_time_graph)
        self.frequency_graph = frequency_graph
        self.input_spectrogram = input_spectro
        self.output_spectrogram = output_spectro
        self.time_domain_X_coordinates = None
        self.time_domain_Y_coordinates = None
        self.slider1 = slider1
        self.slider2 = slider2
        self.slider3 = slider3
        self.slider4 = slider4

    @abstractmethod
    def modify_frequency(self, value: int):
        pass
    def load_signal(self):
        # Load should be implemented for each tab rather than for a certain graph type, and the function should handle 2 cases(.wav, .hea)
        pass
