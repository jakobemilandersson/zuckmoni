% x = Log-table of past stock-prices.
% t = Amount of steps off development.
% n = Number of simulated paths
% dt= Size of each step.
%
% returns: Fkn paths, who gives a fuck right?
%          it plots cool stuff and can make us money.
function paths = future_value_simulator(x, t, n, dt)

%???
XReturns = diff(log(x));
%Mean-value of ???
mu = mean(XReturns);
%t by 100 evenually random numbers.
epsilon = randn(t,n);
sigma = std(XReturns);

%Where magic happens ;)
factors = exp((mu-sigma^2/2)*dt + sigma*epsilon*sqrt(dt));

%Latest price of x, used to simulate future development
lastPriceVector = ones(1,n)*x(end);
%Extend each lastPrice-value with its deveolpment
factors2 = [lastPriceVector;factors];

%Matrix with the develepment-paths
paths = cumprod(factors2);

%----------------------------------------------------------

%Bollinger maddafakka
[mid, uppr, lowr] = bollinger(x,5,0,2);
%closeBolling = [mid.CLOSE, uppr.CLOSE, lowr.CLOSE];
closeBolling = [mid, uppr, lowr];

%----------------------------------------------------------

%Värden för Chaikin oscialltor-funktionen:
highp = max(x);
lowp = min(x);
closep = x(end);
tvolume = 0; %???

chosc = chaikosc(highp, lowp, closep, tvolume);

%----------------------------------------------------------
%Plot all shit
figure;
plot(closeBolling);
figure;
plot(paths);