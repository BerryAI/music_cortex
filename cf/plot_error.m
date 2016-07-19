# Plot the matrix factorization error versus iterations

load 'error.mat'
plot(error);
title('Matrix approximation error versus # iteration');
print -djpg 'error.jpg';
