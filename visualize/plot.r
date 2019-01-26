# javaVMのメモリ拡張
options(java.parameters = "-Xmx5g" )
library(venneuler)

makeTextName <- function(x) {
    return(paste(x,".txt",sep=""))
}

makeIdsFilePath <- function(x){
    return( paste("ids/",makeTextName(x),sep="") )
}

# screen_name から、ファイルを読み込み。ベクトルを返す
readIdsFile <- function(ScreenName){
    f.path <- makeIdsFilePath(ScreenName)
    print(f.path)
    d <- read.table( f.path, header=FALSE, colClasses="character" )
    d <- cbind(d,ScreenName)
    return(d)
}

plotVenn <- function(namec){
    d <- c()
    for( i in 1:length(namec) ){
        d1 <- readIdsFile(namec[i])
        d <- rbind(d,d1)
    }

    names(d) <- c("elements", "sets")

    # twitterユーザー情報を持った外部ファイルからデータの読み込み
    users <- read.csv("users.csv", colClasses="character")

    # screen_name と照らしあわせて、アカウント名を取得
    u.id <- sapply(namec, function(x){which(x == users$screen_name)})

    # ラベル用にわかりやすいアカウント名を代入
    u.name <- users$name[ u.id ]

    # フォロワー数を取得
    u.followers <- c( tapply(d$sets, d$sets, length) )
    u.followers.id <- sapply(namec, function(x){which(x == names(u.followers))})
    u.followers <- u.followers[u.followers.id]
    u.followers.label <- format(u.followers, big.mark=",", scientific=F)

    # ラベルにフォロワー数を追加
    # 取得したアカウント名をlabel変数に代入
    labels <- paste(u.name, u.followers.label, sep="\n")

    v <- venneuler(d, counts=TRUE)
    v$labels <- labels
    plot(v, main="フォロワーの重複度合い")
}

# 読み込むscreen_nameを設定している。
name1 <- "imascg_stage"
name2 <- "lovelive_SIF"
name3 <- "bang_dream_gbp"

namec <- c(name1, name2, name3)

png("venn.png",height=960, width=960, res=144)
plotVenn(namec)
dev.off()
