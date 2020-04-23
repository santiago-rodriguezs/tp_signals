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
muestras = [1:nx];

%Guardo un archivo .wav 
audiowrite('ruidorosa.wav',ruidorosa,fs);

%Ploteo de freqs
freqs = fft(ruidorosa);
P2 = abs(freqs/nx);
P1 = P2(1:nx/2+1);
P1(2:end-1) = 2*P1(2:end-1);
f = fs*(0:(nx/2))/nx;
semilogx(f,P1) 
xlim([20 20000])

