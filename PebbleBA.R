appmet <- read.csv("file.choose"())

attach(appmet)

time <- as.Date(as.POSIXct(date[0:2], origin="1970-01-01", format ="%d"))

g7 <- ggplot(aes(time),identity_user)
g7 + geom_bar(stat="identity") + coord_flip() + theme_bw(base_family = "Avenir", base_size = 10) 
+ labs(title = "Usage Over Time") + labs(x= "Date") + labs(y= "Users")

sapply(time, function(x) length(unique(x)))
/Users/kristen/PebbleBA.R

dayuser <- read.table(file.choose(), sep="," , col.names=c("date", "user"))

#DAU
ggplot(dayuser, aes(dayuser$date, dayuser$user)) + geom_bar(stat="identity") + theme_bw(base_family = "Avenir", base_size = 10) + labs(title = "User Activity") + labs(x= "Date") + labs(y= "DAU")

ggplot(dayuser, aes(dayuser$date, dayuser$user)) + geom_bar(stat="identity", alpha=1/3, color="blue") + theme_bw(base_family = "Avenir", base_size = 10) + labs(title = "User Activity") + labs(x= "Date") + labs(y= "DAU")

#grid-free plot
#DAU
# need to reorder y-axis, reduce tick marks on y-axis, divide by total for percentage
ggplot(dayuser, aes(dayuser$date, as.numeric(as.character(dayuser$user))/270000 *100)) + geom_bar(stat="identity", alpha=1/3, color="blue") + theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank(), panel.background = element_blank(), axis.line = element_line(colour = "black")) + labs(title = "User Activity") + labs(x= "Date") + labs(y= "DAU")

#best DAU plot
ggplot(dayuser2, aes(dayuser2$date, as.numeric(as.character(dayuser2$user))/270000 *100)) + geom_bar(stat="identity", alpha=1/3, color="blue", fill="blue") + theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank(), panel.background = element_blank(), axis.line = element_line(colour = "black")) + labs(title = "User Activity") + labs(x= "Date") + labs(y= "DAU") + coord_cartesian(ylim=c(30, 35))

#3 months
ggplot(dayuser, aes(dayuser$date, as.numeric(as.character(dayuser$user))/270000 *100)) + geom_bar(stat="identity", alpha=1/3, color="blue", fill="blue") + theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank(), panel.background = element_blank(), axis.line = element_line(colour = "black")) + labs(title = "User Activity") + labs(x= "Date") + labs(y= "DAU") + coord_cartesian(ylim=c(30, 45))

#changing from factor value to numeric
as.numeric(as.character(dayuser$user))/270000 *100

#MAU
monthuser <-read.table(file.choose(), sep="," , col.names=c("date", "user"))

ggplot(monthuser, aes(monthuser$date, monthuser$user)) + geom_bar(stat="identity", alpha=1/3, color="blue") + theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank(), panel.background = element_blank(), axis.line = element_line(colour = "black")) + labs(title = "User Activity") + labs(x= "Date") + labs(y= "DAU")


#Cluster
m=as.matrix(cbind(appmet$time, appmet$app_name),ncol=2)
cl=(kmeans(m,3))
cl$size
cl$withinss

appmet$cluster=factor(cl$cluster)
centers=as.data.frame(cl$centers)

ggplot(appmet, aes(x=time, y=appmet$app_name, color=cluster )) + 
  geom_point() + 
  geom_point(data=centers, aes(x=V1,y=V2, color='Center')) +
  geom_point(data=centers, aes(x=V1,y=V2, color='Center'), size=52, alpha=.3, legend=FALSE)


