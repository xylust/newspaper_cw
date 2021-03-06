# Classes methods that allow us to access the data models

from .models import Article, Comment

# Gets the latest 10 articlses from the model
def GetLatestArticles():
    articles = Article.objects.all().order_by('-pub_date')[:10]
    return articles

# Gets all the articles ordered chronologically
def GetAllArticles():
    articles = Article.objects.all().order_by('-pub_date')
    return articles

# Gets the single article by Id
def GetArticleById(id):
    article = Article.objects.get(pk=id)
    return article

# Get all the articles in the specified category
def GetArticlesByCategory(category_filter):
    articles = Article.objects.all().filter(category = category_filter).order_by('-pub_date')
    return articles

# Get the 10 latest articles in the specified category
def GetLatestArticlesByCategory(category_filter):
    articles = Article.objects.all().filter(category = category_filter).order_by('-pub_date')[:10]
    return articles

# Get the category from the parameters
def ExtractCategory(params):
    query = params.get('category')
    return query

def GetCommentsForArticle(id):
   comments = Comment.objects.all().filter(article__id=id)
   return comments 

def GetComment(id):
   comment = Comment.objects.get(pk=id)
   return comment 

