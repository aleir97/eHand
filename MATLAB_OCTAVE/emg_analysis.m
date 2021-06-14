emg_data = xlsread('emg', 'hoja1')';

n = 1:1000;
ch1 = emg_data(1,1:1000);
ch2 = emg_data(2,1:1000);

Fs = 1000;
d = designfilt('bandstopiir','FilterOrder', 2 ,'HalfPowerFrequency1', 59, 'HalfPowerFrequency2', 61, 'DesignMethod','butter','SampleRate',Fs);

ch1 = filtfilt(d,ch1);
ch2 = filtfilt(d,ch2);

figure(1);
subplot(211);
plot(n, ch1);

subplot(212);
plot(n, ch2);
