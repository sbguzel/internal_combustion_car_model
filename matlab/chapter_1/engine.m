dt = 0.0001;

D = @(u, l, r, L) (u * 4 * pi^2 * r^3 * L / 57.2958) / l;
u = 0.02;   % 70C SAE 30
l = 5.2e-5; % oil height m
r = 0.05;   % journal radius m
L = 0.05;   % journal depth m
damping = ((D(u,l,r,L)) * 9 + 4 * 0.05) * 1.5;
inertia = (0.04 + 0.0515 + 0.00125 * 4 + 0.0079 * 4) * 1.5;

sysc = tf(1,[inertia damping 0]);
sysd = c2d(sysc, dt);