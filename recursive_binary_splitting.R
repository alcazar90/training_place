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



find_split <- function(y, x, s) {
  #
  #
  #
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
  output
}

# usage
output <- find_split(y, x, cut_points(x))

p <- data.frame(x = as.double(names(output)), y = output,
                stringsAsFactors = FALSE)

ggplot(p, aes(x = x, y = y)) + geom_line()
output[which.min(output)]






