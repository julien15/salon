#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bottle import  run, request,template,post,route,error
import json
import time
import os
#fonction permettant d'ouvrir la page d'accueil, principalement du html et css
@route('/')
def formulaire():
    c='''
        <!DOCTYPE html>
        <html>
        <head lang="en">
            <meta charset="UTF-8">
            <title> Le salon de la bière </title>
            <style>
                body{
                    background-image:url("http://photos.up-wallpaper.com/images248/euj0c1zssmt.jpg");
                    background-repeat: no repeat;
                    background-size:cover;
                }
                #indentificateur{
                    color:white;
                    text-align:center;
                }
                h1{
                    color:white;
                    font-size:50px;
                    text-align:center;
                }
                a{
                    color:white;
                }
                a:hover{
                    color:rgb(240,245,0);
                }


            </style>
        </head>
        <body>
            <h1>Bienvenue au salon de bière</h1>
            <form method="post" action="/login" id="indentificateur">
                <p>
                <label for="Identifiant">Votre pseudo</label> : <input type="text" name="pseudo" />
                <br/>
                <label for="pass">Mot de passe</label> : <input type="password" name="pass" />
            </p>
            <p><a href="http://localhost:8088/sinscrire"> Pas encore de compte ? </p>
            <input type="submit" value = 'se connecter'/>
            </form>

        </body>
        </html>'''
    return c
#fonction permettant d'ouvrir la page d'inscription, principalement du html et css
@route('/sinscrire')
def formulaire1(note='''<p id="note"></p> '''):
    c='''
        <!DOCTYPE html>
        <html>
        <head lang="en">
            <meta charset="UTF-8">
            <title> Le salon de la bière </title>
            <style>
                body{
                    background-image:url("http://photos.up-wallpaper.com/images248/euj0c1zssmt.jpg");
                    background-repeat: no repeat;
                    background-size:cover;
                    }
                td,tr{
                    color:white;
                }
                #note{
                    color:red;
                    }

            </style>
        </head>
        <body>
        <div align='center'>
            <form method="post" action="/traitement">
                <table>
                <tr>
                    <td><label for="Identifiant">Votre pseudo</label></td> <td><input type="text" name="pseudo"/></td>
                </tr>
                <tr>
                    <td><label for="pass">Mot de passe</label></td><td><input type="password" name="pass"/></td>
                </tr>
                <tr>
                    <td><label for="date">Date de naissance</label></td><td><input type="date" name="date"/></td>
                </tr>
                </table>
            <input type="submit" value = "s'enregistrer"/>'''
    c+=note
    c+='''
            </form>
        </div>

        </body>
        </html>'''
    return c
#fonction permettant de sauvegarder les identifiants et les mots de passe dans la basse de donnée des identifiants
@post("/traitement")
def traitement():
    document=open("indentifiant.txt","r")
    enreg1=json.load(document)
    document.close()
    id=request.forms.get("pseudo")
    mp=request.forms.get("pass")
    date=request.forms.get("date")
    for n in enreg1:
        if id==n:
            note='''<p id="note"> Identifiant dejà choisi</p>'''
            return formulaire1(note)
    l=[]
    l.append(mp)
    l.append(date)
    enreg1[id]=l
    réintegration=open("indentifiant.txt","w")
    réintegration.write(json.dumps(enreg1,sort_keys=True,indent=4,ensure_ascii=False))
    réintegration.close()
    return login()
#fonction permettant de vérifier l'identifiant et son mot de passe 
@post("/login")
def login():
    document=open("indentifiant.txt","r")
    enreg1=json.load(document)
    document.close()
    id=request.forms.get("pseudo")
    mp=request.forms.get("pass")
    for n in enreg1:
        if n == id :
            a=enreg1[n]
            if a[0]== mp:
                return salon()
#fonction permettant d'ouvrir la page principal, principalement du html et css
def salon():
    return template("page-principal.html")
#fonction permettant d'ouvrir la page principal, principalement du html et css
@route("/forum")
def forum():
    document=open("forum.txt",'r')
    enreg=json.load(document)
    document.close()
    # utilisation des fonctions json pour ouvrir la base de donnée du forum
    r='''
    <!DOCTYPE html>
    <html>
    <head lang="en">
        <meta charset="UTF-8">
        <title>forum</title>
        <style>
            body{
                background-image:url("http://photos.up-wallpaper.com/images248/euj0c1zssmt.jpg");
                background-repeat: no repeat;
                background-size:cover;
            }
            h1{
                width:100%;
                color:white;
                text-align:center;
                font-size: XX-large;
                font-family: Lucida Calligraphy;
                }
            article{
                margin-left:10%;
                color:white;
            }
            table{
                border-collapse: collapse;
                margin-left:10%;
            }
            thead{
                color:white;
                text-align:center;

                }

            tbody {

                    border: 1px solid black;
                    color:white;
                    text-align:center;
                }
            th {
                    border: 1px solid black;
                }
            a{
            color:red;
            width:5%;
            }
            a:hover{
                color:white;
                }


        </style>
    </head>
    <body>
        <h1>Forum</h1>
        <a href="http://localhost:8088/salon">Accueil</a>
        <article>
        <form method="post" action="/traitementforum">
        <p>
           <label for="forum">Que penser vous de notre site ?</label><br />
           <textarea name="forum" id="forum"></textarea>
        </p>
        <input type="submit" value = "envoyer"/>
        </form>
        </article>'''
    r+='''
        <table><thead><tr><th colspan="2"><h3>Commentaire</h3></th><tr></thead>'''
    r+='''<tbody>'''
    for n in enreg:
            r+='''<tr><th>{}</th><th>{}</th></tr>'''.format(n,enreg[n])
    r+='''
        </tbody></table>
    </body>
    </html>'''
    #création d'un tableau en fonction de la base de donnée
    return r
#fonction permettant de sauvegarder les écrits des internautes dans la base de donnée du forum
@post("/traitementforum")
def traitementduforum():
    document=open("forum.txt","r")
    enreg1=json.load(document)
    document.close()
    id=request.forms.get("forum")
    enreg1[time.strftime("%d %B %Y %H:%M:%S")]=id
    réintegration=open("forum.txt","w")
    réintegration.write(json.dumps(enreg1,indent=4,ensure_ascii=False))
    réintegration.close()
    return forum()
#fonction tableau permettant d'utiliser les données des bases de données et les mettre dans un tableau
def tableau(a,r,path):
    document=open(path,'r')
    enreg=json.load(document)
    document.close()
    for n in enreg:
        if n==a:
            g=enreg[n]
    r+='''
            <table><caption>Liste des bière '''+a+'''</caption><thead><tr><th>Nom de la bière</th><th>note</th><th>type/fermentation</th> </tr></thead>'''
    r+='''<tbody>'''
    for n in g:
        for t in n:
            p=n[t]
            r+='''
                <tr><th>'''+str(t)+'''</th><th>'''+str(p[0])+'''</th><th>'''+str(p[1])+'''</th> </tr>'''
    r+='''
        </tbody></table></div>
        '''
    return r
#variate de la fonction tableau() mais peut être utiliser plusieur fois dans une même fonction
def tableau2(a,path):
    document=open(path,'r')
    enreg=json.load(document)
    document.close()
    for n in enreg:
        if n==a:
            g=enreg[n]
    b='''
            <table><caption>Liste des bière '''+a+'''</caption><thead><tr><th>Nom de la bière</th><th>note</th><th>type/fermentation</th> </tr></thead>'''
    b+='''<tbody>'''
    for n in g:
        for t in n:
            p=n[t]
            b+='''
                <tr><th>'''+str(t)+'''</th><th>'''+str(p[0])+'''</th><th>'''+str(p[1])+'''</th> </tr>'''
    b+='''
        </tbody></table></div>
        '''
    return b
#fonction permettant d'ouvrir la page contact, principalement du html et css
@route("/contact")
def contact():
    return template("contact.html")
#fonction permettant d'ouvrir la page couleur, principalement du html et css
@route('/couleur')
def couleur():
    return template("couleurs2.html")
#fonction permettant l'ouverture des differentes pages des couleurs, principalement du html et css+utilisationde la fonction tableau()
@route('/couleur/<nom>')
def categoriecouleur(nom):
    if nom=="blonde":
        r='''
        <!DOCTYPE html>
        <html>
        <head lang="en">
            <meta charset="UTF-8">
            <title> Bière blonde </title>
            <style>
                h1 {
                    color : white;
                    font-size:50px;
                    text-align: center;
                    font-family:Lucida Calligraphy;
                    font-style: italic;
                }
                h2{
                    color : white;
                    font-size:40px;
                    text-align: center;
                }
                #intro{
                    width=33%;
                }
                a{
                color:red}
                u{
                text-decoration: underline;
                }
                p{
                    color: white;
                    font-size:20px;
                    font-family:Comic sans ms;
                    font-style: italic;
                    margin-left:60px;
                    margin-top:40px;
                }
                body{
                    background-image: url("http://waquid.com/wp-content/uploads/2015/07/bi%C3%A8re1.jpg");
                }
                section{
                    width:40%
                }
                #basededonné{
                    color:white;
                }
                table{
                    border-collapse: collapse;
                    color:red;
                }
                td, th {
                    border: 1px solid black;
                    color:white;
                }

            </style>
        </head>
        <body>
            <h1> La bière blonde</h1>
            <p> <a href="http://localhost:8088/salon"> >Acceuil</a> </p>
            <section>
                <p> La blonde,</p>
                <p>Bière existant depuis les origines de la bière et brassée avec du froment ou de l'avoine en plus de l'orge. Cela leur donne un goût légèrement piquant. Les blanches sont également souvent brassées comme autrefois avec des épices : coriandre, curaçao, écorces d’orange. Elles peuvent être de fermentation haute ou basse (plus rare) et sont généralement refermentées en bouteille.</p>
                <p><u>Quelques exemples:</u></p>
                <p>
                    Hoegaarden - Vedett - Moinette - Omer - Ciney - Leffe blond
                </p>
                <div align="center">'''
        y=tableau("Blonde",r,"traitement.txt")
        return y
    if nom=="brune":
        r='''
        <!DOCTYPE html>
        <html>
        <head lang="en">
            <meta charset="UTF-8">
            <title> Bière brune </title>
            <style>
                    h1 {
                    color : white;
                    font-size:50px;
                    text-align: center;
                    font-family:Lucida Calligraphy;
                    font-style: italic;

                }
                h2{
                    color : white;
                    font-size:40px;
                    text-align: center;
                }
                #intro{
                    width=33%;
                }
                a{
                color:red}
                u{
                text-decoration: underline;
                }
                p{
                    color: white;
                    font-size:20px;
                    font-family:Comic sans ms;
                    font-style: italic;
                    margin-left:60px;
                    margin-top:40px;
                }
                body{
                    background-image: url("http://chimay.com/wp-content/uploads/2015/01/chimay_bleue1.jpg");
                    background-repeat:no repeat;
                    background-size:cover;
                }
                section{
                    width:40%
                }
                #basededonné{
                    color:white;
                }
                table{
                    border-collapse: collapse;
                    color:red;

                }
                td, th {
                    border: 1px solid black;
                    color:white;
                }

            </style>
        </head>
        <body>
            <h1> La bière brune</h1>
            <p> <a href="http://localhost:8088/salon"> >Acceuil</a> </p>
            <section>
                <p> La bière brune,</p>
                <p>Bière existant depuis les origines de la bière et brassée avec du froment ou de l'avoine en plus de l'orge. Cela leur donne un goût légèrement piquant. Les blanches sont également souvent brassées comme autrefois avec des épices : coriandre, curaçao, écorces d’orange. Elles peuvent être de fermentation haute ou basse (plus rare) et sont généralement refermentées en bouteille. photo@chimay</p>
                <p><u>Quelques exemples:</u></p>
                <p>
                    Vedett - Moinette - Omer - Chimay bleu - Leffe brune
                </p>
            </section>
            <div align="left">'''
        return tableau("Brune",r,"traitement.txt")

    if nom=="ambree":
        r='''
            <!DOCTYPE html>
            <html>
            <head lang="en">
            <meta charset="UTF-8">
            <title> Ambree </title>
            <style>
                    h1 {
                        color : white;
                        font-size:50px;
                        text-align: center;
                        font-family:Lucida Calligraphy;
                        font-style: italic;

                    }
                    h2{
                        color : white;
                        font-size:40px;
                        text-align: center;
                    }
                    #intro{
                        width=33%;
                    }
                    a{
                    color:red}
                    p{
                        color: white;
                        font-size:20px;
                        font-family: Comic sans ms;
                        font-style: italic;

                    }
                    body{
                        background-image: url("http://www.brasserie-lagermanoise.fr/DataGermanoise/downloads/Media/19_Fotolia_61530573_M.jpg");
                        background-repeat:no repeat;
                        background-size:cover;
                    }
                    section{
                        width:40%;
                        margin-top:60px;
                        margin-left:30%;

                    }
                    table{
                    border-collapse: collapse;
                    color:red;

                    }
                    td, th {
                    border: 1px solid black;
                    color:white;
                    }
            </style>
            </head>
            <body>
            <h1> La bière ambrée </h1>
            <p> <a href="http://localhost:8088/salon"> >Acceuil</a> </p>
            <section>
                <p> La bière ambrée,</p>
                <p> Après la première guerre mondiale, s'inspirant des anglais, beaucoup de brasseurs belges passent de la lager brune traditionnelle à la bière de type « lager » (bière de fermentation haute). Cette bière, à la robe bronze ou rouge-ambrée à cuivrée, est une bière légère, qui se boit souvent comme alternative à la pils, avec une teneur en alcool comparable (5°). Elle possède une saveur douce, un petit goût de levure et une légère touche épicée. La plupart d'entr'elles ont un léger apport de houblon et un arôme légèrement fruité, voire caramelisé. Presque toutes sont filtrées et pasteurisées, et à part la couleur, les ales ambrées belges n'ont que peu de choses en commun avec les ales anglaises. </p>
                <p><u>Quelques exemples:</u></p>
                <p>
                    Orval - Lilly Blue - Gouden Carolus - Bush - Gauloise - Chimay Rouge
                </p>
            </section>
            <div align="center">'''
        return tableau("Ambree",r,"traitement.txt")

    if nom=="blanche":
        r='''
        <!DOCTYPE html>
        <html>
        <head lang="en">
            <meta charset="UTF-8">
            <title> Bière Blanche </title>
            <style>
                    h1 {
                        color : white;
                        font-size:50px;
                        text-align: center;
                        font-family:Lucida Calligraphy;
                        font-style: italic;

                    }
                    h2{
                        color : white;
                        font-size:22.5px;
                        margin-left:60px;
                        margin-top:40px;
                        font-family:Comic sans ms;
                        font-style: italic;

                    }
                    #intro{
                        width=33%;
                    }
                    a{
                    color:red}
                    p{
                        color: white;
                        font-size:15px;
                        font-family:Comic sans ms;
                        font-style: italic;
                        margin-left:60px;
                        margin-top:40px;
                    }
                    body{
                        background-image: url("http://www.parketdekor.be/images/backgrounds/bg_03.jpg");
                        background-repeat:no repeat;
                        background-size:cover;
                    }
                    section{
                        width:40%
                        margin-top:&60px;
                        margin-right:1100px;
                    }
                    article{
                        position: absolute;
                        right: 150px;
                        bottom: 220px;
                    }

                    table{
                    border-collapse: collapse;
                    color:red;

                    }
                    td, th {
                    border: 1px solid black;
                    color:white;
                    }

            </style>
            </head>
            <body>
            <h1> La blanche</h1>
            <p> <a href="http://localhost:8088/salon"> >Acceuil </a></p>
            <section>
                <h2> La blanche,</h2>
                <p>
                    La bière rouge est souvent assimilé aux bières fruités car ça couleur(rouge)est ainsi retrouvé dans la gamme de bières kreik par exemple.
                </p>
                <h2> Porters & origine des Stouts </h2>
                <p> Les bières blanches sont des bières brassées avec une forte proportion de froment malté ou non. Il existe deux grandes traditions de bière « blanche » : en Belgique (Witbier ou Tarwebier) et en Bavière (Weizenbier). Les bavaroises ne contiennent que du malt et du houblon ; différents niveaux de torréfaction du malt différencient les catégories Hell (claire) et Dunkel (sombre). La catégorie Hell filtrée est appelée Kristall. Le nom de la « blanche » entraîne souvent une confusion due à une proximité phonétique des mots allemands Weizen (froment) et Weiß (blanc). Il se peut bien qu'au Moyen Âge les méthodes de fabrication des deux bières se ressemblaient fortement. Cependant de nos jours nous nous trouvons en face de deux types de bières très différentes. Les bières d'origine allemande sont toujours brassées à base de malt de froment ainsi que du houblon, mais elles ne contiennent jamais d'autres épices ni de céréales non maltées. La Weizenbier ou Weissbier (terme bavarois pour Weizenbier) peut donc être considérée comme une autre sorte de bière, tout comme les Gueuzes qui sont troubles et contiennent elles aussi du froment, mais ne sont pour cela pas appelées « blanches ». Les bières blanches produites dans les autres pays sont le plus souvent proches de la bière blanche belge.@wikipedia
                </p>
                <h2>On retrouve plusieurs variantes;</h2>
                <p>Blanche de Namur - Hoegaarden Blanc - Limburgs witte - chimay blanche </p>
            </section>

            <article>
                <iframe width="840" height="472.5" src="https://www.youtube.com/embed/CWqFxoONwrc" frameborder="0" allowfullscreen></iframe>
            </article>
            <div align="center">'''
        return tableau("Blanche",r,"traitement.txt")
    if nom=="rouge":
        r='''
            <!DOCTYPE html>
            <html>
            <head lang="en">
            <meta charset="UTF-8">
            <title> Bière Rouge </title>
            <style>
                    h1 {
                        color : white;
                        font-size:50px;
                        text-align: center;
                        font-family:Lucida Calligraphy;
                        font-style: italic;

                    }
                    h2{
                        color : white;
                        font-size:22.5px;
                        margin-left:60px;
                        margin-top:40px;
                        font-family:Comic sans ms;
                        font-style: italic;

                    }
                    #intro{
                        width=33%;
                    }
                    a{
                    color:red}
                    u{
                    text-decoration: underline;
                    color: white;
                    font-size:15px;
                    font-family:Comic sans ms;
                    font-style: italic;
                    margin-left:60px;
                    margin-top:40px;
                    }
                    p{
                        color: white;
                        font-size:15px;
                        font-family:Comic sans ms;
                        font-style: italic;
                        margin-left:60px;
                        margin-top:40px;
                    }
                    body{
                        background-image: url("http://www.fondsdecranhd.com/wallpapers/rouge_1680x1050.jpg");
                        background-repeat:no repeat;
                        background-size:cover;
                    }
                    section{
                        width:40%
                        margin-top:60px;
                        margin-left:1100px;
                    }
                    article{
                        position: absolute;
                        left: 150px;
                        bottom: 220px;
                    }
                    table{
                        border-collapse: collapse;
                        color:red;

                    }
                    td, th {
                        border: 1px solid black;
                        color:white;
                    }

            </style>
            </head>
            <body>
            <h1> La rouge</h1>
            <p> <a href="http://localhost:8088/salon"> >Acceuil </a></p>
            <section>
                <h2> La rouge,</h2>
                <p>
                    La bière rouge est souvent assimilé aux bières fruités car ça couleur(rouge)est ainsi retrouvé dans la gamme de bières kriek par exemple.
                </p>
                <h2> Porters & origine</h2>
                <p> La bière rouge est un type de bière belge flamande à fermentation mixte : la fermentation haute est suivie pour une partie du brassin d'une fermentation spontanée secondaire en foudre de chêne, pendant au moins 18 mois. Le produit final est obtenu en mélangeant la bière « jeune » plus sucrée, et la bière « vieillie » plus acide. L'utilisation de malt caramélisé foncé lui donne sa couleur caractéristique. Peu alcoolisée, elle a un goût aigre-doux et est parfois aromatisée à la cerise comme la Kriek. On la confond souvent avec la vieille brune (ou oud bruin, laquelle ne subit pas de matûration en fûts de bois, mais en cuves ouvertes - généralement du plastique ou du métal). En résumé, les bières rouges sont souvent des bières quisont fruité donc n'ailant pas de degré d'alcool élevé.@wikipedia
                </p>
                <h2>On retrouve plusieurs variantes;</h2>
                <p>Kriek (Liefmans/Lindemans/Belle-Vue) - Kasteel rouge - la gamme Floris - La Rouge</p>

            </section>
            <article>
                <iframe width="840" height="472.5" src="http://media.meltybuzz.fr/article-2666298-desktop/media.mp4" type="video/mp4" frameborder="0" allowfullscreen></iframe>

            </article>
            <div align="center">'''
        return tableau("Rouge",r,"traitement.txt")
    if nom =="noire":
        r='''
            <!DOCTYPE html>
            <html>
            <head lang="en">
            <meta charset="UTF-8">
            <title> Bière noire </title>
            <style>
                    h1 {
                        color : white;
                        font-size:50px;
                        text-align: center;
                        font-family:Lucida Calligraphy;
                        font-style: italic;

                    }
                    h2{
                        color : white;
                        font-size:22.5px;
                        margin-left:60px;
                        margin-top:40px;
                        font-family:Comic sans ms;
                        font-style: italic;

                    }
                    #intro{
                        width=33%;
                    }
                    a{
                    color:red}
                    u{
                    text-decoration: underline;
                    color: white;
                    font-size:15px;
                    font-family:Comic sans ms;
                    font-style: italic;
                    margin-left:60px;
                    margin-top:40px;
                    }
                    p{
                        color: white;
                        font-size:15px;
                        font-family:Comic sans ms;
                        font-style: italic;
                        margin-left:60px;
                        margin-top:40px;
                    }
                    body{
                        background-image: url("http://storage.journaldemontreal.com/v1/dynamic_resize/sws_path/jdx-prod-images/81ebc872-7504-4c5a-be2d-691a3d5e772c_ORIGINAL.jpg?quality=80&version=15&size=968x");
                        background-repeat:no repeat;
                        background-size:cover;
                    }
                    section{
                        width:40%
                        margin-top:60px;
                        margin-left:1100px;
                    }
                    article{
                        position: absolute;
                        left: 150px;
                        bottom: 220px;
                    }
                    table{
                        border-collapse: collapse;
                        color:red;

                    }
                    td, th {
                        border: 1px solid black;
                        color:white;
                    }

            </style>
            </head>
            <body>
            <h1> La noire</h1>
            <p> <a href="http://localhost:8088/salon"> >Acceuil </a></p>
            <section>
                <h2> La noire,</h2>
                <p>
                    Brisons enfin le secret de la fabrication d’une des bière les plus réputées, celle qui fait le bonheur de nos soirées rugby, celle qui se vend à allure frénétique dans les bons vieux pubs irlandais, celle qui se vend dans des canettes draught, celle qui attire certains autant qu’elle en repousse d'autres, celle qui est représentée par la Guinness, mais qui peut porter bien d’autres noms, celle qui porte souvent l’étendard vert-blanc-orange mais qui se fabrique ailleurs, notamment au pays de la baguette, enfin, celle qui coupe la faim autant qu’elle ravive la soif. La stout est noire, parce qu’elle est faite à partir d’une grande quantité de malt d’orge torréfiée et/ou d’orge crue torréfiée, très torréfiée, ce qui explique les goût chocolatés et caféinés. Son amertume s’explique par l’utilisation du houblon et de l’orge torréfiée. Voyons comment différencier une stout d'une autre…
                </p>
                <h2> Porters & origine des Stouts </h2>
                <p> Les porters sont des bières très brunes apparues en Angleterre au XVIIIème. Favorites des Londoniens jusqu'au milieu du XIXème siècle, elles se font plus rares ensuite à cause de la montée en puissance des bitters puis de l'arrivée des lagers.
                    A l'époque, une brasserie pouvait faire différents porters et stout était un adjectif qui désignait souvent la plus forte : "stout porter" (stout signifie étymologiquement "brave" et fut utilisé pour qualifié des bières "fortes" dans plusieurs styles brassicoles). On pouvait aussi trouver des extra porters et des double porters (par ordre croissant de force). Cependant, d'une brasserie à une autre, une double pouvait être plus forte qu'une stout, un brasseur pouvait aussi n'avoir qu'une seule bière et l'appeler simplement porter alors qu'elle pouvait être aussi forte que la plupart des stouts… bref stout n'était pas une désignation absolue et donc faire la différence entre une stout et un porter est relativement vain… Mais le débat subsiste sur l'origine exacte des deux mots et leurs différences, nous ne attarderons pas plus sur le sujet…
                    Par usage, "stout" s'est retrouvé utilisé seul et désigne aujourd'hui un style mondialement connu de bières.
                </p>
                <h2>On retrouve plusieurs variantes;</h2>
                <p>Irish/Dry Stouts - Chocolate Stouts - Coffee Stouts - Imperial Stouts - Sweet Stouts</p>
            </section>
            <article>
                <iframe width="840" height="472.5" src="https://www.youtube.com/embed/B5UedfCySQk" frameborder="0" allowfullscreen></iframe>
            </article>
            <div align="center">'''
        return tableau("Noire",r,"traitement.txt")
#fonction permettant d'ouvrir la page type, principalement du html et css + utilisation de la fonction tableau2()
@route("/type")
def type():
    r='''
        <!DOCTYPE html>
        <html>
        <head lang="en">
        <meta charset="UTF-8">
        <title> Bières simple/double/triple/quadruple </title>
        <style>
                h1 {
                    color : white;
                    font-size:50px;
                    text-align: center;
                    font-family:Lucida Calligraphy;
                    font-style: italic;

                }
                h2{
                    color : white;
                    font-size:22.5px;
                    margin-left:60px;
                    margin-top:40px;
                    font-family:Comic sans ms;
                    font-style: italic;

                }
                #intro{
                    width=33%;
                }
                a{
                color:white}
                p{
                    color: white;
                    font-size:15px;
                    font-family:Comic sans ms;
                    font-style: italic;
                    margin-left:60px;
                    margin-top:40px;
                }
                body{
                    background-image: url("http://www.fondsdecranhd.com/wallpapers/rouge_1680x1050.jpg");
                    background-repeat:no repeat;
                    background-size:cover;
                }
                section{
                    width:40%
                    margin-top:60px;
                    margin-left:1100px;
                }
                article{
                    position: absolute;
                    left: 150px;
                    bottom: 220px;
                }
                table{
                    border-collapse: collapse;
                    color:red;

                }
                td, th {
                    border: 1px solid black;
                    color:white;
                }
            </style>
            </head>
            <body>
            <h1> Les fermentations</h1>
            <p> <a href="http://localhost:8088/salon"> >Acceuil </a></p>
            <section>
            <p>
                Comme vous le sachez, le brassage d'une bière peut se faire de différentes manières. On laisse fermenter plus/moin longtemps, on rajoute différents ingrédients en plus, etc.. Si on s'interesse à la façcon dont on peut laisser fermenter une bière (cad le processus qui "gère" le degré d'alcool). On peut  ainsi faire fermenter une bière un certain nombre de fois pour obtenir les propriétées souhaitées. Plus on fait fermenter une bière, plus elle sera alcoolisée. Une bière qui a subi une seule fermentation peut être assimilé a-à une bière simple. 2 ferentations = bière double. 3 fermentations = bière triple. Et enfin la quadruple qui elle a subi 4 fermentations.
            </p>
            <h2> Porters & origine </h2>
            <p>Historiquement, on désigne par simple, double et triple (enkel, dubbel et tripel) les diverses bières brassées au sein d'un monastère : simple (légère, pour les moines), double avec plus de malt (corsée, pour les abbés) et triple avec encore plus de malt (forte, pour les convives). La simple était aussi souvent appelée la « petite bière » ou « bière de table ». Elle était parfois brassée à l'aide du moût obtenu par le rinçage des drêches.
                C'est en 1856 qu'une bière de fermentation haute dans le style des bières trappistes de l'abbaye de Westmalle est à l'origine de l'usage moderne de ces appellations. On les emploie pour des bières dont la teneur en alcool est supérieure à celle d'une bière de consommation courante, qui serait qualifiée de « simple ». Les brasseurs jouent sur la quantité des matières premières utilisées pour un même volume d'eau, lors des différentes phases de création, pour obtenir un moût, plus ou moins concentré en sucre, qui donnera une bière plus ou moins forte en alcool. Ce type de bière est généralement brassé à partir d'une grande quantité de sucre ajouté, permettant d'atteindre le degré alcoolique souhaité après fermentation avec une plus petite quantité de grain.Les bières à fermentation spontanée utilisent des levures sauvages (levures circulant naturellement dans l'air capturé à l'aide de moût laissé en plein air).Une bière double est en général une bière de garde, de titre alcoolique de l'ordre de 7 % en volume. Une bière triple est une bière blonde, ambrée (par ex : Bush Ambrée Triple) ou brune (par ex : Abbaye d'Aulnes Brune 8), au froment (ex : Grosse Bertha) de titre alcoolique de l'ordre de 9 % ou supérieur en volume.Ces termes, auxquels s'ajoute aussi quadruple ou « Abt », sont également utilisés dans les bières d'abbaye ; ces brasseries utilisent un autre type de classification pour indiquer la force de bières de ce style, notamment par les bières de Maredsous.L’appellation triple est une bière qui a subi une fermentation primaire, la fermentation secondaire et la troisième fermentation en bouteille1.Enfin, l'appellation « double » ou « triple » est parfois utilisée comme une technique de marketing pour désigner une bière qui aurait subi deux ou trois fermentations successives. Cette pratique est parfois considérée comme incohérente dans la mesure où la majorité des bières subissent au moins une fermentation primaire, transformant le sucre en alcool, et une fermentation secondaire (période de garde) permettant l'affinage du goût de la bière. C'est cet affinage, qui peut avoir lieu en plusieurs phases, et notamment se poursuivre en bouteille pour une bière sur levure, qui a amené certaines brasseries à parler de « triple fermentation », bien que cette appellation ne soit pas préférée par certains amateurs de bière. Si bien qu'il existe des doubles à triple fermentation, et inversement
                ®wikipedia
            </p>
            <h2>exemples;</h2>
            <p>trappe triple/quadruple, triple karmeliet, Koninck</p>
            </section>
            <article>
            <iframe width="840" height="472.5" src="https://www.youtube.com/embed/VIXN5xARVA4" frameborder="0" allowfullscreen></iframe>
            </article>'''
    r+='''<div align="center">'''
    y=tableau2("Trappiste","traitement2.txt")
    r+=y
    r+='''<div align="left">'''
    y=tableau2("Triple","traitement2.txt")
    r+=y
    r+='''<div align="right">'''
    y=tableau2("Simple","traitement2.txt")
    r+=y
    r+='''<div align="center">'''
    y=tableau2("Double","traitement2.txt")
    r+=y
    r+='''<div align="left">'''
    y=tableau2("Houblon","traitement2.txt")
    r+=y
    r+='''<div align="right">'''
    y=tableau2("D'Abbaye","traitement2.txt")
    r+=y
    r+='''<div align="center">'''
    y=tableau2("Quadruple","traitement2.txt")
    r+=y
    return r
#fonction permettant d'ouvrir la page pils, principalement du html et css+utilisation de la fonction tableau()
@route("/pils")
def pils():
    r='''
        <!DOCTYPE html>
        <html>
        <head lang="en">
            <meta charset="UTF-8">
            <title> Pils </title>
            <style>
                    h1 {
                        color : white;
                        font-size:50px;
                        text-align: center;
                        font-family:Lucida Calligraphy;
                        font-style: italic;

                    }
                    h2{
                        color : white;
                        font-size:40px;
                        text-align: center;
                    }
                    #intro{
                        width=33%;
                    }
                    a{
                    color:red
                    }
                    u{
                    text-decoration: underline;
                    }

                    p{
                        color: white;
                        font-size:20px;
                        font-family: Comic sans ms;
                        font-style: italic;
                        margin-left:60px;
                        margin-top:40px;

                    }
                    body{
                        background-image: url("http://waquid.com/wp-content/uploads/2015/07/bi%C3%A8re1.jpg");
                        background-repeat:no repeat;
                        background-size:cover;
                    }
                    section{
                        width:40%;
                    }
                    article{
                        position: absolute;
                        right: 200px;
                        bottom: 300px;
                    }
                     table{
                        border-collapse: collapse;
                        color:red;

                    }
                    td, th {
                        border: 1px solid black;
                        color:white;
                    }


            </style>
        </head>
        <body>
            <h1> La pils </h1>
            <p> <a href="http://localhost:8088/salon"> >Acceuil</a> </p>
            <section>
                <p> La pils ou pilsner,</p>
                <p> Même si la Belgique est célèbre pour ses bières spéciales, ce sont les pils qui sont les plus vendues sur le marché interne et en exportation. Les pils représentent 75 % de la production de bières belges. De fermentation basse, on les reconnaît aisément à leur couleur claire et leur goût doux.
                    La marque la plus connue internationalement est Stella Artois, tandis que Jupiler et Maes sont les plus populaires sur le marché interne, ainsi que la (sainte) Carapils pour les étudiants! </p>
                <p>
                    La pils est une bière de basse fermentation, blonde dorée au goût légèrement amer. Elle est filtrée et saturée, possède en moyenne 5% de volume d'alcool et se déguste bien fraîche. En raison de son caractère désaltérant, ce style de bière a acquis une très grande popularité parmi les consommateurs.
                    L'appellation «pils» provient de la ville de Pilsen (République Tchèque), où ce style de bière vit le jour en 1842. Au fil des années, la pils se répandit à travers toute l'Europe Germanophone. En Belgique, la production débuta en 1928 avec le brassage de la Cristal, suivie un an plus tard par l'apparition de la Stella.
                    Style de bière très populaire en Belgique, d'aucuns considèrent aussi la pils comme une «bière de soif». Les heures de gloire de la pils se situent d'ailleurs entre 1900 et 1968, période où la consommation ne fit qu'augmenter.
                    Depuis le début des années septante, les bières de haute fermentation (spéciales, trappiste,...) ont connu un regain d'intérêt notoire chez les consommateurs. Les statistiques des dernières années confirment une augmentation de la consommation de bières spéciales au détriment des pils, même si ces dernières continuent à être vendues en masse.
                    En Belgique, le marché de la pils est dominé par les brasseries industrielles. Cependant, soulignons l'émergence de pils artisanales produites par des moyennes et micro-brasseries, ce qui contribue à renouveler les styles de pils et offrir au consommateur un regard différent sur la bière.
                </p>
                <p><u>Quelques exemples:</u></p>
                <p>
                    Jupiler - Meas - Stella Artois - Cristal - Primus - Carapils - 365
                </p>
            </section>
            <article>
                <iframe width="840" height="472.5" src="https://www.youtube.com/embed/SGoVjhJCjJs" frameborder="0" allowfullscreen></iframe>
            </article>'''
    r+='''<div align="center">'''
    y=tableau("Pils",r,"traitement2.txt")
    return y
#fonction util en cas d'erreur 404
@error(404)
def erreur404():
        r='''
        <!DOCTYPE html>
<html>
<head lang="en">
    <meta charset="UTF-8">
    <title>Erreur 404 </title>
    <style>
        body{
            background-image:url(http://apollo-eu-uploads.s3.amazonaws.com/1440122138/maxresdefault.jpg);
        }
        h1{
            color:white;
        }
    </style>
</head>
<body>
    <h1>Error 404</h1>

</body>
</html>'''
        return r
#fonction util en cas d'erreur 405
@error(405)
def erreur405():
        r='''
        <!DOCTYPE html>
        <html>
        <head lang="en">
        <meta charset="UTF-8">
        <title>Erreur 405 </title>
        <style>
            body{
            background-image:url(http://apollo-eu-uploads.s3.amazonaws.com/1440122138/maxresdefault.jpg);
            }
            h1{
                color:white;
            }
        </style>
        </head>
        <body>
            <h1>Error 405</h1>

        </body>
        </html>'''
        return r
#fonction permettant d'acceder à la page d'accueil plus facilement
@route("/")
def lien():
    r='''
    <!DOCTYPE html>
        <html>
        <head lang="en">
        <meta charset="UTF-8">
        <title></title>
        <style>
            body{
            background-image:url("http://waquid.com/wp-content/uploads/2015/07/bi%C3%A8re1.jpg");
            }
            h2{
                color:white;
            }
            a{
            color:red;
            }
            a:hover{
            color:white;
            }
        </style>
        </head>
        <body>
            <h2> pour rejoindre notre site veillez cliquer sur ce lien :
            </br>
            <a href="http://localhost:8088/salon"> Salon de la bière</a>
        </body>
        </html>'''
    return r
run(host='0.0.0.0', port=int(os.environ.get('PORT', 5005)))
