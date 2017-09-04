library(ISLR)

# prepare data example for continuos variables
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


# toy example to test the categorical criterias
toy <- data.frame(high_degree = c("Bachelors", "Masters", "Masters", "PhD", "PhD",
                                  "Bachelors", "Bachelors", "PhD", "Bachelors",
                                  "Masters", "Masters", "PhD", "Masters", "Bachelors"),
                  work_exp = c("Mobile Dev", "Web Dev", "Mobile Dev", "Mobile Dev",
                               "Web Dev", "UX Design", "Mobile Dev", "Web Dev",
                               rep("UX Design", 3), "Mobile Dev", "Mobile Dev",
                               "Web Dev"),
                  fav_language = c("Objective-C", "Java", "Java", rep("Objective-C", 3),
                                   "Java", "Objective-C", "Java", "Objective-C",
                                   rep("Java", 3), "Objective-C"),
                  work_visa = c("TRUE", "FALSE", rep("TRUE", 4), rep("FALSE", 3), "TRUE",
                                "FALSE", "FALSE", "TRUE", "TRUE"),
                  hire = c(rep("yes", 4), "no", "no", "yes", "no", "yes", "no", "yes",
                           "no", "yes", "no"))
                  

freq <- function(x) {
  # Input: x, a factor (categorical) vector
  # Return the frequency for each level
  labels <- unique(x)
  output <- vector("double", length(labels))
  for (i in 1:length(output)) {
    output[i] <- sum(x == labels[i]) / length(x)
    names(output)[i] <- levels(labels)[i]
  }
  output
}

# verify the gini index calculation in this link:
# https://stats.stackexchange.com/questions/77213/computing-the-gini-index
gini_index <- function(x) {
  # Input: x, a vector containing the frequency for the levels of
  #         a categorical variable
  # Return the gini index for the given categorical variable
  output <- vector("double", length(x))
  for (i in length(output)) {
    p <- x[i]
    output[i] <- p ^ 2
  }
  1 - sum(output)
}

entropy <- function(x) {
  # Input: x, a vector containing the frequency for the levels of
  #         a categorical variable
  # Return the entropy for the given categorical variable
  output <- vector("double", length(x))
  for (i in length(output)) {
   p <- x[i] 
   output[i] <- -p * log2(p)  
  }
  sum(output)
}

# compute the entropy and the gini index criteria at the root node (all data)
entropy(freq(toy$hire))
gini_index(freq(toy$hire))

# compute the entropy citeria after resolve the root note; suppose that
# the variable selected as root node was "hire", and now we are compute
# the criteria for the variable "high_degree"
df <- toy[, c("high_degree", "hire")]
by_level <- split(df, df$high_degree)
lapply(by_level, function(df) entropy(freq(df$hire)))
lapply(by_level, function(df) gini_index(freq(df$hire)))


# Recursive binary splitting/partition
# ==========================================================================
# 1. Select the variable:
#  which minimize in the most quantity in the
# case of continuos variables the RSS or gain the maximum information
# in the case of categorical variables

# 2. Split the data:
# based in cut point of the selected variable in case of continuos variables
# or in the category that...

# 3. Repeat the previous process (step 1 + 2) on the new created region
# left or right but be consistent

# 4. Create a stop criteria based on the number of observations
# that contain the regions

recursive_binary_splitting(y, X, var = NULL) {
  # create data structure
  if (var == NULL) {
    selected_info <- select_var(y, X)
    var_to_split <- selected_info$var
    opt_point <- selected_info$split_point
  } else {
    
  }
  temp <- select_(y, X)
  var_to_split <- temp$var
  point_to_split <- temp$split_point
  if (criterio) {
    # 
  } else {
    # dsasda
  }
}


