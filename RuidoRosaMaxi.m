%Defino cantidad de Muestras
nx = 2^16;

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
ruido = x(nt60+1:end);

Fs = 44100;
audiowrite('ruido.wav',ruido*0.8,Fs,'Comment','Este es mi nuevo archivo de audio','Artist','UNTREF');
