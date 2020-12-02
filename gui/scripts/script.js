const favAnimeText = document.querySelector("#fav-anim");
const animeList = document.querySelector("#animeList");
var container = document.querySelector(".form-container");
var i = 0; 

function addToList(){
    var currentAnime = favAnimeText.value;

    if (currentAnime === ''){
        document.querySelector("#animemsg").innerHTML = 'No items to add';
    }
    else {
        document.querySelector("#animemsg").innerHTML = '';
        var animeEntry = document.createElement('li');

        var deleteLink = document.createElement('a');
        deleteLink.appendChild(document.createTextNode('Delete'));
        deleteLink.setAttribute('href', '#');
        deleteLink.setAttribute('id', 'dlanime'+i);
        deleteLink.setAttribute('class', 'deleteLink');
        deleteLink.setAttribute('onclick', 'deleteAnime(' + i + ')');
    
        animeEntry.setAttribute('id', 'anime'+i);
        i++;
        animeEntry.appendChild(document.createTextNode(currentAnime));
        animeEntry.appendChild(deleteLink);
        animeList.appendChild(animeEntry);
        
        favAnimeText.value = '';
        console.log(currentAnime);

    }

}

function deleteAnime(x){
    var targetAnime = document.querySelector("#anime"+x);
    var targetAnimeDel = document.querySelector("#dlanime"+x);
    console.log(targetAnimeDel);
    console.log(targetAnime);
    targetAnime.remove();
    targetAnimeDel.remove();

}
document.querySelector("#addToFav").onclick = addToList;