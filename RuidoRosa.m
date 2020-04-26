%Defino la duracion en segundos del ruido:
duracion = 10;
fs = 44100;
nx = duracion * fs;

%Defino valores para el filtro
B = [0.049922035 -0.095993537 0.050612699 -0.004408786];
A = [1 -2.494956002 2.017265875 -0.5221894];

%Tiempo para que la señal caiga -60dB
nt60  = round(log(1000) / (1-max(abs(roots(A)))));

%Genero un vector de valores aleatorios
v = randn(1, nx + nt60);

%Se aplica el filtro
x = filter(B,A,v);

%Ruido Rosa
ruidorosa = x(nt60+1:end);

%Guardo un archivo .wav 
audiowrite('ruidorosa.wav',ruidorosa,fs);
