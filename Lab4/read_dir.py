import os
import struct
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

from Lab4.estimates import output_dir

PATH = 'rawData'


class Frame:
    def __init__(self, data, stop_point):
        self.data = data
        self.stop_point = stop_point
        self.timestamp = None
        self.reserved = None


class Bin:
    def __init__(self, lvl):
        self.lvl = lvl[0]
        self.last = lvl[1]
        self.side = int
        self.mode = int
        self.frame_count = int
        self.reserved = None
        self.frames = []

    def file_header(self, file):
        header = file.read(256)
        side, mode, frame_count = struct.unpack('3B', header[:3])
        return [side, mode, frame_count]

    def file_frames(self, file):
        with open(f'{file}', 'rb') as fid:
            self.side, self.mode, self.frame_count = self.file_header(fid)
            for _ in range(self.frame_count):
                stop_point = struct.unpack('H', fid.read(2))[0]
                timestamp = struct.unpack('I', fid.read(4))[0]  # not working
                reserved = np.fromfile(fid, dtype=np.uint16, count=5)  # for future
                rawdata = np.fromfile(fid, dtype=np.uint16, count=8192).reshape(1024, 8)
                ch18 = np.zeros((1024, 8), dtype=rawdata.dtype)
                for ch in range(8):
                    ch18[:, ch] = np.roll(rawdata[:, ch], stop_point)
                self.frames.append(ch18)
        return self.frames


class rawData:
    def __init__(self, path: str, calibrate=False):
        print('path = ', Path(path).absolute())
        self.file_dir = Path(path).absolute().glob('*.bin')
        print('dir = ', self.file_dir)
        self.bins = []
        self.lvls = []
        if "ADC" in path:
            self.date = path.split("ADC")[0]
        else:
            self.date = "None"
        self.calibrate_flag = calibrate
        print('finish ctor')

    def file_lvl(self, file):
        print('in file lvl')
        filename = file.__str__().split("\\")[-1]
        print(f'file name = {file.__str__()}')
        if not self.calibrate_flag:
            if "lvl" in filename:
                lvl = [float(filename.split("_lvl")[0])]
            else:
                lvl = [float(filename.split("_side")[0])]
        else:
            if "lvl" in filename:
                lvl = [(filename.split("_lvl")[0])]
            else:
                lvl = [(filename.split("_side")[0])]

        if (filename.split(".bin")[0]).split("data")[1]:
            lvl.append(True)
        else:
            lvl.append(False)

        return lvl

    def get_bin_by_lvl(self, lvl, last=False):
        for k in range(len(self.bins)):
            if self.bins[k].lvl == lvl:
                if last == self.bins[k].last:
                    return self.bins[k]
                else:
                    continue
        print("NO LVL SUCH AS INPUT")
        return None

    def read_directory(self):
        headers_info = []
        print('reading directory')
        for file in self.file_dir:
            print('here')
            bin_file = Bin(self.file_lvl(file))
            print('here 2')
            bin_file.file_frames(file)
            self.bins.append(bin_file)
            self.lvls.append(bin_file.lvl)

            headers_info.append([[bin_file.lvl, bin_file.last], [bin_file.side, bin_file.mode, bin_file.frame_count]])
        print(f'headers info = {headers_info}')
        return headers_info


    # отсюда сохранение

    def hist_bin_by_lvl_frame_channel(self, lvl: float, frame: int, channel: int, last=False):
        bin_file = self.get_bin_by_lvl(lvl, last)
        if bin_file:
            plt.hist(np.array(bin_file.frames[frame])[:, channel],
                     color="lightcoral",
                     edgecolor="darkred",
                     bins=128,
                     density=True)
            plt.title(f"lvl: {lvl}, frame: {frame}, channel: {channel + 1}")
            plt.grid(True, linestyle="--", alpha=0.7)
            file_name = f"hist_lvl_{lvl}_frame_{frame}_channel_{channel + 1}.png"
            plt.savefig(file_name)
            plt.show()
            print(f"Histogram saved as {file_name}")
        else:
            print("input data wrong format")

    def plot_bin_by_lvl_frame_channel(self, lvl, frame: int, channel: int, last=False):
        bin_file = self.get_bin_by_lvl(lvl, last)
        if bin_file:
            plt.plot(np.array(bin_file.frames[frame])[:, channel],
                     color="#074c3a")
            plt.title(f"lvl: {lvl}, frame: {frame}, channel: {channel + 1}")

            # Сохранение графика
            file_name = f"plot_lvl{lvl}_frame{frame}_channel{channel + 1}.png"
            file_path = os.path.join(output_dir, file_name)
            plt.savefig(file_path)
            print(f"График сохранён в {file_path}")

            plt.show()
        else:
            print("input data wrong format")

    def hist_bin_by_lvl_frame_all_bins(self, lvl: float, frame: int, last=False):
        bin_file = self.get_bin_by_lvl(lvl, last)
        if bin_file:
            plt.figure(figsize=(12, 6))
            colors = ["#FF5733", "#33FF57", "#3357FF", "#FF33A1",
                      "#A133FF", "#33FFF5", "#F5FF33", "#FF8C33"]
            for channel in range(0, 8):
                plt.subplot(2, 4, channel + 1)
                plt.hist(np.array(bin_file.frames[frame])[:, channel],
                         color=colors[channel],
                         edgecolor="black",
                         bins=1024,
                         density=True)
                plt.title(f"{lvl, frame, channel + 1}")

            # Сохранение графика
            file_name = f"hist_all_channels_lvl{lvl}_frame{frame}.png"
            file_path = os.path.join(output_dir, file_name)
            plt.savefig(file_path)
            print(f"График сохранён в {file_path}")

            plt.show()
        else:
            print("input data wrong format")

    def plot_bin_by_lvl_frame_all_bins(self, lvl, frame: int, flag=True, last=False):
        bin_file = self.get_bin_by_lvl(lvl, last)
        if bin_file:
            if flag:
                plt.figure(figsize=(12, 6))
                cmap = plt.colormaps["plasma"]
                colors = [cmap(i / 7) for i in range(8)]  # Разделяем диапазон на 8 цветов
                for channel in range(0, 8):
                    plt.subplot(2, 4, channel + 1)
                    plt.grid(True, linestyle="--", alpha=0.7)
                    plt.plot(np.array(bin_file.frames[frame])[:, channel],
                             color=colors[channel], alpha=0.8)
                    plt.title(f"{lvl, frame, channel + 1}")

                # Сохранение графика
                file_name = f"plot_all_channels_lvl{lvl}_frame{frame}.png"
                file_path = os.path.join(output_dir, file_name)
                plt.savefig(file_path)
                print(f"График сохранён в {file_path}")

                plt.show()
            else:
                cmap = plt.colormaps["plasma"]
                colors = [cmap(i / 7) for i in range(8)]  # Разделяем диапазон на 8 цветов

                for channel in range(0, 8):
                    plt.plot(np.array(self.get_bin_by_lvl(lvl).frames[frame])[:, channel],
                             color=colors[channel], label=f"channel {channel + 1}", alpha=0.8)
                plt.title(f"{lvl, frame}")
                plt.legend()
                plt.grid(True, linestyle="--", alpha=0.7)
                # Сохранение графика
                file_name = f"plot_overlay_channels_lvl{lvl}_frame{frame}.png"
                file_path = os.path.join(output_dir, file_name)
                plt.savefig(file_path)
                print(f"График сохранён в {file_path}")

                plt.show()
        else:
            print("input data wrong format")


rawData_instance = rawData(PATH)
rawData_instance.read_directory()

rawData_instance.plot_bin_by_lvl_frame_all_bins(0.225, 3)
rawData_instance.plot_bin_by_lvl_frame_all_bins(0.225, 3, False)

