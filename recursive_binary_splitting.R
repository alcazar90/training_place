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


for (i in 1:length(var)) {
  
}

