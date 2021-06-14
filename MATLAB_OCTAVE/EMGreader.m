clear;

% Inicialización del puerto serie
puerto_serial = serialport('COM5', 115200);
flush(puerto_serial);

configureTerminator(puerto_serial,"CR/LF");
puerto_serial.Timeout = 5;

warning('off', 'MATLAB:serial:fscanf:unsuccessfulRead');

% Vector de muestras con ventana 256
y = zeros(1, 1000);
n = 1:1:1000;

disp('ENTER:')
pause();

write(puerto_serial,1,"uint8")
readline(puerto_serial)

for i = 1 : 1000
    
y(i) = str2double(readline(puerto_serial));

end

figure;
stem(n, y); 
hold on; 
%plot(n, y, 'r');
xlabel ('muestra'); ylabel('Amplitud');
title('EMG');

FID = fopen('MEASURE.txt', 'w');
if FID == -1, error('Cannot create file.'); end
fprintf(FID, '%s\t\r\n', 'med1');
fprintf(FID, '%g\t\r\n', y);

fclose(FID);

delete(puerto_serial);





