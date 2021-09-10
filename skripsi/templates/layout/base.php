{% comment %} file template global yang akan menjadi wadah bagi file template di view lainnya {% endcomment %}
<!DOCTYPE html>
<html lang="en">

<head>

    {% include "layout/head.html" %}
    {% comment %} {% extends "layout/head.html" %} {% block content %} {% endcomment %}
    <style>
        body .row {
            font-size: 0.8rem;
        }
    </style>

</head>

<body data-spy="scroll" data-target=".mainmenu-area">
    <!-- Preloader-content -->
<div class="preloader">
    <span><i class="lnr lnr-sun"></i></span>
</div>

<nav class="mainmenu-area" data-spy="affix" data-offset-top="200">
    <div class="container-fluid">
        <div class="navbar-header">
            <button type="button" class="navbar-toggle" data-toggle="collapse" data-target="#primary_menu">
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
            </button>
            <!-- <a class="navbar-brand" href="#"><img src="/static/appy/appy/images/logo.png" alt="QA"></a> -->
        </div>
        <div class="collapse navbar-collapse" id="primary_menu">
            <ul class="nav navbar-nav mainmenu">
                <li class="active"> <a href="#home_page">QA</a> </li>
                <li><a href="#answer">          Answer          </a></li>
                <li><a href="#preprocessing">   Pre-processing  </a></li>
                <li><a href="#word_graph">      Word Graph      </a></li>
                <li><a href="#cnn">             CNN             </a></li>
                <li><a href="#title">           Title           </a></li>
            </ul>
        </div>
    </div>
</nav>

<header class="home-area" id="home_page">

<!-- --------------------------------Qustion-------------------------------------- -->
<div class="container">
    <div class="row">
        <div class="col-xs-12 col-md-6 col-sm-offset-3 text-center">
            <h1 class="wow fadeInUp " data-wow-delay="0.4s" style="color:black">QAs on WIKIPEDIA<h1>
            <h4 class="wow fadeInUp " data-wow-delay="0.4s" style="color:black">Question and answer system themed about history and mathematical scientists with the wikipedia knowledge base</h4>
          
                
        </div>
        <div class="col-xs-12 col-sm-10 col-sm-offset-1">
            <div class="subscribe-form text-center">       
                <form class="wow fadeInUp " data-wow-delay="0.4s" action="/semua/" method="POST">
                    {% csrf_token %}
                    <h4 class="blue-color"> 
                        <input type="text" class="control" placeholder="Enter your question" required  name="question" >
                    </h4>
                    <button class="bttn-white active" type="submit" value="search"><span class="lnr lnr-location"></span> Search</button> 
                    
                    {% comment %} <button type="submit" class="btn btn-primary">Cari</button> {% endcomment %}
                </form>
                
                <div class="space-20"></div>
                {% if request.answer_sparql.answer_sparql == None and answer_wikipedia.answer_wikipedia == None %}
                        <h4 clasS="dark-color wow fadeInUp"  data-wow-delay="0.4s">No Answer</h4>
                {% else %}
                    <a href="#answer" class="bttn-default wow fadeInUp" data-wow-delay="0.8s"><span class="lnr lnr-arrow-down"></span>ANSWER</a> 
                    <h4 clasS="dark-color wow fadeInUp"  data-wow-delay="0.4s">
                        SPARQL : 
                        - KEY {{answer_sparql.sum_key_answer}} &nbsp;&nbsp;&nbsp;&nbsp;f
                    </h4>
                {% endif %}
                
            </div>
            
        </div>
    </div>
</div>
</header>


{% if wrong_topics != None %}
<div class="container">
        <div class="modal fade in" id="myModal" role="dialog" style="display: block; padding-right: 19px;">
            <div class="modal-dialog modal-md" style="overflow-y: scroll; max-height:85%; margin-top: 50px; margin-bottom:50px;">
            <div class="modal-content">
                <div class="modal-header">
                <button type="button" class="close" data-dismiss="modal">&times;</button>
                <h4 class="modal-title" style="color:black;">Sorry your question topic is not detected. Please enter the topic you want</h4>
                <h4 class="modal-title blue-color">{{wrong_topics}}</h4>
                </div>
                <div class="modal-body">
                <form class="wow fadeInUp " data-wow-delay="0.4s" action="/get_topic/" method="POST">
                    {% csrf_token %}
                    <h4 class="blue-color"> 
                        <input type="text"  placeholder="Enter your topics" required  name="topic" >
                    </h4>
                </div>
                <div class="modal-footer">
                <button class="bttn-white active" type="submit" value="search"></span> submit</button> 
                </div>
                </form>

            </div>
            </div>
        </div>
</div>
{% endif%}


{% if option_topics != None %}
<div class="container">
        <div class="modal fade in" id="myModal" role="dialog" style="display: block; padding-right: 19px;">
            <div class="modal-dialog modal-md" style="overflow-y: scroll; max-height:85%; margin-top: 50px; margin-bottom:50px;">
            <div class="modal-content">
                <div class="modal-header">
                <button type="button" class="close" data-dismiss="modal">&times;</button>
                <h4 class="modal-title">TITLE</h4>
                </div>
                <div class="modal-body">
                <form class="wow fadeInUp " data-wow-delay="0.4s" action="/get_title/" method="POST">
                    {% csrf_token %}
                    {% for opt in option_topics %}
                        <h4 class="blue-color"><input type="radio" name="titless" value="{{opt}}" required > &nbsp{{opt}}</h4>
                    {% endfor %}
                </div>
                <div class="modal-footer">
                <button class="bttn-white active" type="submit" value="search"></span> save</button> 
                </div>
                </form>

            </div>
            </div>
        </div>
</div>
{% endif%}





<section class="section-padding" id="answer">
        <div class="container">
            <div class="row">
                <div class="col-xs-12 col-md-12">
                    <div class="page-title text-center">
                    <h2 class="blue-color wow fadeInUp" data-wow-delay="0.4s">ANSWER</h2>
                    <h3 class="DARk-color wow fadeInUp" data-wow-delay="0.4s">{{Question}}</h3>
                    
                    <h4 class="DARk-color wow fadeInUp" data-wow-delay="0.4s">Article : <a href={{answer_wikipedia.url}}>  {{finally_title}} </a> </h4>

                    
                        <div class="space-20"></div>
                        <h4 class="wow fadeInUp " data-wow-delay="0.4s" style="color:black; text-align:justify">
                            <!-- {{answer_sparql.answer_sparql}}
                            {{answer_wikipedia.answer_wikipedia}} -->
                            <ul>
                                {% for as in answer_sparql.answer_sparql %}
                                    <li> <h4 style="color:black"> {{as}} </h4></li>
                                {% endfor %}
                                {% for aw in answer_wikipedia.answer_wikipedia %}
                                    <li> <h4 style="color:black"><B>{{aw.0}}</B> , {{aw.2}} </h4></li>
                                {% endfor %}
                            </ul>
                        <h4>
                    
                    </div>
                </div>
            </div>
        </div>
    </section>




<!-- --------------------------------PREPROCESSING-------------------------------------- -->
<section class="section-padding" id="preprocessing">
    <div class="container">
        <div class="row">
            <div class="col-xs-12 col-sm-8 col-sm-offset-2">
                <div class="page-title text-center">
                    <h2 class="blue-color wow fadeInUp" data-wow-delay="0.4s">Pre-processing</h2>
                    {% comment %} <h5 class="title">Features</h5> {% endcomment %}
                    {% comment %} <h3>Pwoerful Features As Always</h3> {% endcomment %}
                    <h4 class=" dark-color wow fadeInUp" data-wow-delay="0.2s"> The process for identifying keywords from the question sentence </h4>
                    <div class="space-10"></div>
                    <h5 class=" dark-color wow fadeInUp" data-wow-delay="0.2s"><b>Key Word : </b> {{result_preprocessing.key_word|join:" "}}  </h5>
                    <h5 class=" dark-color wow fadeInUp" data-wow-delay="0.2s"><b>lexical Word : </b> {{result_preprocessing.lexical_word|join:", "}}  </h5>
                </div>
            </div>
        </div>

        <div class="row">
            
            <div class="col-xs-12 col-sm-4">
                <div class="space-60 hidden visible-xs"></div>
                <div class="service-box wow fadeInUp" data-wow-delay="0.2s">
                    <div class="box-icon">
                        <i class="lnr lnr-pencil"></i>
                    </div>
                    <h4>Tokenizing</h4>
                    <h5 style="color:black">
                        <ul>
                            {% for k in result_preprocessing.result_tokenizing %}
                                
                                <li> {{ k }} </li>
                            {% endfor %}
                        </ul>
                    <h5>
                </div>
                <div class="space-50"></div>
                <div class="service-box wow fadeInUp" data-wow-delay="0.2s">
                    <div class="box-icon">
                        <i class="lnr lnr-bug"></i>
                    </div>
                    <h4>Stopwords</h4>
                    <h5 style="color:black">
                        {{result_preprocessing.result_stopword|join:", "}}
                    <h5>
                </div>
            </div>
            <div class="col-xs-12 col-sm-4 ">
                <div class="space-60 hidden visible-xs"></div>
                <div class="service-box wow fadeInUp" data-wow-delay="0.2s">
                    <div class="box-icon">
                        <i class="lnr lnr-spell-check"></i>
                    </div>
                    <h4>POS (Part of Speech)</h4>
                    <h5 style="color:black">
                        {% for k in result_preprocessing.result_POS %}
                            <li>{{ k|join:" - "}} </li>
                        {% endfor %}
                    <h5>
                </div>

                
                <div class="space-50"></div>
                <div class="service-box wow fadeInUp" data-wow-delay="0.2s">
                    <div class="box-icon">
                        <i class="lnr lnr-hourglass"></i>
                    </div>
                    <h4>Chuncked</h4>
                    <h5 style="color:black">
                        <ul>
                            {% for k in result_preprocessing.result_chuncked %}
                                <li> {{ k }} </li>
                            {% endfor %}
                        </ul>
                    <h5>
                </div>
                <div class="space-50"></div>


            </div>
            <div class="col-xs-12 col-sm-4 ">
                <div class="space-60 hidden visible-xs"></div>
                <div class="service-box wow fadeInUp" data-wow-delay="0.2s">
                    <div class="box-icon">
                        <i class="lnr lnr-tag"></i>
                    </div>
                    <h4>NER (Name Entity Recognition)</h4>
                    <h5 style="color:black">
                        
                        {{ result_preprocessing.result_ner}}
                    <h5>
                </div>


                <div class="space-50"></div>
                <div class="service-box wow fadeInUp" data-wow-delay="0.2s">
                    <div class="box-icon">
                        <i class="lnr lnr-list"></i>
                    </div>
                    <h4 class="blue-color">Lemmatization</h4>
                    <h5 style="color:black">
                        {{result_preprocessing.lexical_word|join:", "}} 
                    <h5>
                </div>
            </div>
            
           
        </div>
    </div>
</section>

<!-- --------------------------------WORD GRAPH-------------------------------------- -->
<section class="section-padding" id="word_graph">
    <div class="container">
        <div class="row">
            <div class="col-xs-12 col-sm-8 col-sm-offset-2">
                <div class="page-title text-center">
                    <h3 class="blue-color wow fadeInUp" data-wow-delay="0.4s">Word Graph</h3>
                    {% comment %} <h5 class="title">Features</h5> {% endcomment %}
                    {% comment %} <h3>Pwoerful Features As Always</h3> {% endcomment %}
                    <h4 class=" dark-color wow fadeInUp" data-wow-delay="0.2s"> The process for identifying keywords from the question sentence </h4>
                    <div class="space-10"></div>
                </div>
            </div>
        </div>


        <div class="row">
            <div class="col-xs-12">
                <div class="team-slide">
                    <!-- {{result_graph_word.result_graph_word}} -->
                    {% for x  in result_graph_word.result_graph_word %}
                        {% for x,y  in x.items %}
                            <div class="team-box">
                                <h4 style="text-transform: uppercase;">{{ x }}</h4>
                                <h6 style="color:black; text-align: justify;">
                                        {{y|join:", "}}  
                                </h6>      
                            </div>
                        {% endfor %}
                    {% endfor %}
                </div>
            </div>
        </div>


    </div>
</section>


<section class="section-padding" id="cnn">
    <div class="container">
        <div class="row">
            <div class="col-xs-12 col-sm-6">
                <div class="page-title">
                    <div class="space-10"></div>
                    <h3 class="blue-color wow fadeInUp" data-wow-delay="0.4s">Convolutional Neural Network</h3>
                    <h4 class="dark-color wow fadeInUp" data-wow-delay="0.4s">one method of machine learning from the development of Multi Layer Perceptron (MLP) that is designed to process data two-dimensional. CNN is included in the kind of Deep Neural Network because it level network</h4>
                </div>
            </div>
            <div class="col-xs-12 col-sm-6 col-md-5 col-md-offset-1">
                <div class="space-60 hidden visible-xs"></div>
                {% for z  in result_cnn.class %}
                <div class="service-box wow fadeInUp" data-wow-delay="0.2s">
                    <div class="box-icon">
                        <i class="lnr lnr-rocket"></i>
                    </div>
                    <h4 style="color:black">{{z.1}}</h4>
                </div>
                <div class="space-50"></div>
                {% endfor %}
            </div>
        </div>
    </div>
</section>
<!-- --------------------------------TITLE WIKIPEDIA-------------------------------------- -->
<section class="section-padding" id="title">
    <div class="container">
        <div class="row">
            <div class="col-xs-12">
                <div class="page-title text-center">                   
                    <h3 class="blue-color wow fadeInUp" data-wow-delay="0.4s">Title Wikipedia</h3>
                    <div class="space-10"></div>
                    <h4 class=" dark-color wow fadeInUp" data-wow-delay="0.2s"> Ttitle extraction on wikipedia by means of N-Gram </h4>
                    <h4 class=" dark-color wow fadeInUp" data-wow-delay="0.2s"> the topics discussed are 
                        <b> <a href={{answer_wikipedia.url}}>  {{finally_title}} </a> </b>
                    </h4>
                    
                    <h4 class="DARk-color wow fadeInUp" data-wow-delay="0.4s">
                        
                    </h4>
                    <div class="space-10"></div>
                </div>
            </div>
        </div>
        <div class="row">
            <div class="col-xs-12 col-sm-6">
                <div class="price-box">
                    <div class="price-header">
                        <div class="price-icon">
                            <span class="lnr lnr-moon"></span>
                        </div>
                        <h4 class="upper">Unigram</h4>
                    </div>
                    <div style="text-align:justify:">
                        <h5  style="text-align:justify; color:black;">
                            {% for z  in result_title.unigram %}
                                {% for x,y  in  z.items %}
                                <b> {{x}} </b> :  {{y|join:", "}}
                                <br><br>
                                {% endfor %}
                            {% endfor %}
                        </h5>
                    </div>
                </div>
                <div class="space-30 hidden visible-xs"></div>
            </div>
            <div class="col-xs-12 col-sm-3">
                <div class="price-box">
                    <div class="price-header">
                        <div class="price-icon">
                            <span class="lnr lnr-heart"></span>
                        </div>
                        <h4 class="upper">Bigram</h4>
                    </div>
                    <div style="text-align:justify:">
                        <h5  style="text-align:justify; color:black;">
                            {% for z  in result_title.bigram %}
                                {% for x,y  in  z.items %}
                                <b> {{x}} </b> :  {{y|join:", "}}
                                <br><br>
                                {% endfor %}
                            {% endfor %}
                        </h5>
                    </div>
                </div>
                <div class="space-30 hidden visible-xs"></div>
            </div>
            <div class="col-xs-12 col-sm-3">
                <div class="price-box">
                    <div class="price-header">
                        <div class="price-icon">
                            <span class="lnr lnr-leaf"></span>
                        </div>
                        <h4 class="upper">Trigram</h4>
                    </div>
                    <div style="text-align:justify:">
                        <h5  style="text-align:justify; color:black;">
                            {% for z  in result_title.trigram %}
                                {% for x,y  in  z.items %}
                                <b > {{x}} </b> :  {{y|join:", "}}
                                <br><br>
                                {% endfor %}
                            {% endfor %}
                        </h5>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>

   
    
    {% include "layout/js.html" %} {% block inline_js %} {% endblock %}
    {% comment %} {% extends "layout/js.html" %} {% block inline_js %}{% endblock %} {% endcomment %}
</body>
</html>