library(ggplot2)
library(ISLR)

# prepare data example
df <- ISLR::Hitters[, c("Salary", "Years", "Hits")]
row.names(df) <- NULL
df$Salary <- log(df$Salary)

# remove the observation with missing values in the response variable
df <- df[!is.na(df$Salary), ]
x <- df$Years
y <- df$Salary

split_data <- function(X, var, val) {
  # Input: X, a data frame of the predictor variables 
  #   var, the name of the variable in which the data will be split
  #   val, the value in which the data will be separate
  # Return a list of two elements. The first one is the portion given by
  # the left region of the cut point value ("val"), and the second, is 
  # the right region of the cut point value
  # (FOR NOW THIS IMPLEMENTATION ONLY WORK WITH CONTINUOS VARIABLES
  # AS RESPONSE AND PREDICTORS)
  subset_vector <- X[[var]] < val
  left_region <- X[subset_vector, ]
  right_region <- X[!subset_vector, ]
  list(r1 = left_region, r2 = right_region)
}


cut_points <- function(x) {
  # Input: a vector with the values of a predictor variable
  # Return the cut points to search the space for the optimal
  #   cut point, the one that minimize the RSS of the two regions
  to_s <- sort(x)
  to_s <- unique(to_s)
  s <- vector("double", length(to_s) - 1)
  i <- 1
  while (i < length(to_s)) {
    s[i] <- (to_s[i + 1] + to_s[i]) / 2
    i <- i + 1
  }
  s
}

optimal_point <- function(y, x, s) {
  # Input: y, response variable
  #   x, the predictor variable to split
  #   s, cut-points to evaluate
  # Return the optimal cut point, this is the point that minimize
  # the cost function (RSS of both region)
  output <- vector("double", length(s))
  for (i in 1:length(s)) {
    half_plane <- x > s[i]
    yhat1 <- mean(y[half_plane])
    yhat2 <- mean(y[!half_plane])
    e1 <- y[half_plane] - yhat1
    e2 <- y[!half_plane] - yhat2
    RSS1 <- sum(e1 ^ 2)
    RSS2 <- sum(e2 ^ 2)
    RSST <- RSS1 + RSS2
    output[i] <- RSST
    names(output)[i] <- s[i]
  }
  list(metric = min(output), cut_point = as.double(names(which.min(output))))
}

optimal_point(y, x, cut_points(x))


select_var <- function(y, X) {
  # Input: y, the response variable
  #  X, the predictor variables
  # Return the selected variable, the variable with the minimum RSS and
  # the respectively split point
  metric <- vector("double", ncol(X))
  cp_star <- vector("double", ncol(X))
  for (i in 1:ncol(X)) {
    # so for each variable we need the minimal metric and the optimal
    # cut-point that produce the minimal metric
    temp <- optimal_point(y, X[[i]], cut_points(X[[i]]))
    metric[i] <- temp$metric
    cp_star[i] <- temp$cut_point
  }
  list(var = names(X)[which.min(metric)], split_point = cp_star[which.min(metric)])
}

t <- select_var(y, df[, c(2, 3)])
split_data(df, t$var, t$split_point)




# usage
output <- find_split(y, x, cut_points(x))

p <- data.frame(x = as.double(names(output)), y = output,
                stringsAsFactors = FALSE)

ggplot(p, aes(x = x, y = y)) + geom_line()
output[which.min(output)]






