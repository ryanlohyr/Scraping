PROJECT_NAME ?= 
SPIDER_NAME ?= 
SPIDER_URL ?= 

startproject:
	@echo "Creating project structure..."
	scrapy startproject $1

generatespider:
	@echo "Generating spider..."
	@cd $1 && scrapy genspider $2 $3

crawl:
	@echo "Crawling data..."
	@cd $1 && scrapy crawl $2