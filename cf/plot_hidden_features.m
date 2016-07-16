# Plot the first three hidden features of all songs

load 'hidden_features.mat'
f = hidden_features;
scatter3(f(:,1), f(:,2), f(:,3),[], f(:,1));
xlabel('x_1');
ylabel('x_2');
zlabel('x_3');
title('The first 3 hidden features of all songs from collaborative filtering');
print -djpg 'hidden_features3.jpg';
