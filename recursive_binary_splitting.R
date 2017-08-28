#load libraries
library(ggplot2)

mtcars

# prepare some example data with 2-d feature space to build
# a tree regresion model
X <- mtcars[c(3, 6)]
row.names(X) <- NULL
y <- mtcars[1]
row.names(y) <- NULL


ggplot(X, aes(X$disp, X$wt)) +
  geom_point(data = y, aes(colour = y$mpg))


# realizar la busqueda de la constante que separe el predictor en las
# dos regiones que tengan la mínima suma de los errores cuadrados. 

# Se requiere guardar todas las variables predictoras
var <- names(X)

# para cada variable buscar la constante "s" que separe en dos la variable
# creando dos regiones en cuyo dominio se computa primero el promedio y 
# luego la suma de los errores cuadrados

for (i in 1:length(var)) {
  # iterar por todas las variables predictoras  
}

# primera pregunta, ¿donde inicializar la constante?
var1 <- X[var[1]]

# computar el valor mínimo y máximo de los valores que tiene la variable 
# a splitear
min_val <- min(var1)
max_val <- max(var1)

# estos valores funcionan como limites dado que cualquier constante que tome
# el mismo valor dejará todos los valores del vector en una sola región. Es
# decir, no habrá una partición, o al menos no habrá una partición con los
# valores de la variable de la data de entrenamiento.
min_val
max_val

# Por lo tanto, un approach es inicializar la constante 's' en el valor 
# mínimo y luego, a medida que corre el algoritmo, ir actualizando 's'
# en torno al parametro constante que llamaremos 'alpha'
s <- min_val
alpha <- 0.02

# una vez definido la constante hay que computar la SRC de cada región, esto
# se podría hacer de la siguiente manera por región:
half_plane1 <- var1 > s
half_plane2 <- var1 <= s
yhat1 <- mean(y[half_plane1], na.rm = TRUE)
yhat2 <- mean(y[half_plane2], na.rm = TRUE)
e1 <- y - yhat1
e2 <- y - yhat2
SRC1 <- sum(e1 ^ 2)
SRC2 <- sum(e2 ^ 2)
SRCT <- SRC1 + SRC2

# El proceso anterior hay que repetirlo por cada variable predictora y 
# asegurarse de conservar la información de la constante "s" que entrega
# el menor valor de SRCT de cada variable Xj para luego determinar cual
# es la que minimiza una mayor cantidad...

library(ISLR)
df <- ISLR::Hitters
df <- df[, c("Salary", "Years", "Hits")]
row.names(df) <- NULL
# remove NA from the response variable
df <- df[!is.na(df$Salary), ]
y <- df["Salary"]
y <- log(y)
X <- df[, c("Years", "Hits")]

var <- X[1]
min_val <- min(var)
max_val <- max(var)
s <- min_val
alpha <- 0.2
# create a vector to store the s - SRCT values
output <- vector("double", (max_val - min_val) / alpha)
j = 1
while (s < max_val) {
  half_plane <- var > s
  yhat1 <- mean(y[half_plane])
  yhat2 <- mean(y[!half_plane])
  e1 <- y[half_plane] - yhat1
  e2 <- y[!half_plane] - yhat2
  SRC1 <- sum(e1 ^ 2)
  SRC2 <- sum(e2 ^ 2)
  SRCT <- SRC1 + SRC2
  # store the results
  output[j] <- SRCT
  names(output)[j] <- s
  # update s and j
  s <- s + alpha
  j <- j + 1
}






for (i in 1:length(var)) {
  var <- X[var[i]]
  min_val <- min(var)
  max_val <- max(var)
  s <- min_val
  alpha <- 0.02
  # create a vector to store the s - SRCT values
  output <- vector("double", (max_val - min_val) / alpha)
  j = 1
  while (s <= max_val) {
    half_plane <- var > s
    yhat1 <- mean(y[half_plane])
    yhat2 <- mean(y[!half_plane2])
    e1 <- y[half_plane] - yhat1
    e2 <- y[!half_plane] - yhat2
    SRC1 <- sum(e1 ^ 2)
    SRC2 <- sum(e2 ^ 2)
    SRCT <- SRC1 + SRC2
    # store the results
    output[j] <- SRCT
    names(output)[j] <- s
    # update s and j
    s <- s + alpha
    j <- j + 1
  }
}










library(ISLR)
library(tidyverse)

df <- ISLR::Hitters
df <- tbl_df(df)
df <- df %>% select(Salary, Years, Hits)

df %>% 
  filter(Years < 4.5) %>% 
  mutate(Salary = log(Salary)) %>% 
  summarize(Avg_salary = mean(Salary, na.rm = TRUE))

df %>% 
  filter(Years >= 4.5,
         Hits < 117.5) %>% 
  mutate(Salary = log(Salary)) %>% 
  summarize(Avg_salary = mean(Salary, na.rm = TRUE))

df %>% 
  filter(Years >= 4.5,
         Hits > 117.5) %>% 
  mutate(Salary = log(Salary)) %>% 
  summarize(Avg_salary = mean(Salary, na.rm = TRUE))












