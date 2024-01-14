function query() {

    const views_url = "static/icons/views.png";
    const likes_url = "static/icons/likes.png";
    const dislikes_url = "static/icons/dislikes.png";
    const favorites_url = "static/icons/favorites.png";

    const th = JSON.parse( search_results_intermediate_th );
    const ti = JSON.parse( search_results_intermediate_ti );
    const ct = JSON.parse( search_results_intermediate_ct );
    const p = JSON.parse( search_results_intermediate_p );
    const vc = JSON.parse( search_results_intermediate_vc );
    const s = JSON.parse( search_results_intermediate_s );
    const ids = JSON.parse( search_results_intermediate_i );

    let number_of_search_results = th.length;

    for (i = 0; i < number_of_search_results; i++) {

      let box = document.createElement('div');

      if (number_of_search_results==1){

        box.innerHTML =` 
      
        <div class="main-container" style="border-top: solid 1px black;border-right: solid 1px black;
                                           border-left: solid 1px black;border-bottom: solid 1px black;
                                           border-radius: 10px 10px 10px 10px;
                                           margin-top:275px;
                                           position: absolute;
                                           left:50%;
                                           margin-left:-500px;">
  
              <br>

              <a href="/video/`+ids[i]+`">
  
              <div class="search-container" style="margin-bottom:20px;margin-top:20px;">
  
                  <div class="search-thumbnail">
  
                      <img class="search-thumbnail-image" src=` + th[i] + `>
  
                  </div>
  
                  <div class="search-description">
  
                      <div class="search-description-title">
                          
                          <p class="search-description-title-text">`+ti[i]+`</p>
  
                      </div>
  
                      <div class="search-description-channel">
  
                          <div class="search-description-channel-left">
  
                              <p class="search-description-channel-left-text">` + ct[i] + ` &#183; Upload Date : `+p[i]+` </p>
  
                          </div>
  
                          <div class="search-description-channel-right">
  
                              <img class="search-description-channel-right-image" src=` + views_url + `>
  
                              <p class="search-description-channel-right-text"> &#183; `+vc[i]+` Views</p>
  
                          </div>
  
                      </div>
  
                    <div class="third-line-description">

                        <div class="third-line-description-favorite">

                            <img class="third-line-image-2" src=` + favorites_url + `>

                            <p class="third-line-text">`+s[i].favoriteCount+` </p>

                        </div>

                        <div class="third-line-description-likes">

                            <img class="third-line-image-3" src=` + likes_url + `>

                            <p class="third-line-text"> `+s[i].likeCount+` </p>

                        </div>

                        <div class="third-line-description-dislikes">

                            <img class="third-line-image-4" src=` + dislikes_url + `>

                            <p class="third-line-text"> `+s[i].dislikeCount+` </p>

                        </div>

                    </div>
  
                  </div>
  
              </div>

              </a>
  
              <br>
  
          </div>`;

      }

      else if (i==0){

        box.innerHTML =` 
      
        <div class="main-container" style="border-top: solid 1px black;border-right: solid 1px black;
                                           border-left: solid 1px black;border-radius: 10px 10px 0px 0px;
                                           margin-top:` + 275 + `px;
                                           position: absolute;
                                           left:50%;
                                           margin-left:-500px;">
  
              <br>

              <a href="/video/`+ids[i]+`">
  
              <div class="search-container" style="margin-top:20px;">
  
                  <div class="search-thumbnail">
  
                      <img class="search-thumbnail-image" src=` + th[i] + `>
  
                  </div>
  
                  <div class="search-description">
  
                      <div class="search-description-title">
                          
                          <p class="search-description-title-text">`+ti[i]+`</p>
  
                      </div>
  
                      <div class="search-description-channel">
  
                          <div class="search-description-channel-left">
  
                              <p class="search-description-channel-left-text">` + ct[i] + ` &#183; Upload Date : `+p[i]+` </p>
  
                          </div>
  
                          <div class="search-description-channel-right">
  
                              <img class="search-description-channel-right-image" src=` + views_url + `>
  
                              <p class="search-description-channel-right-text"> &#183; `+vc[i]+` Views</p>
  
                          </div>
  
                      </div>
  
                    <div class="third-line-description">

                        <div class="third-line-description-favorite">

                            <img class="third-line-image-2" src=` + favorites_url + `>

                            <p class="third-line-text">`+s[i].favoriteCount+` </p>

                        </div>

                        <div class="third-line-description-likes">

                            <img class="third-line-image-3" src=` + likes_url + `>

                            <p class="third-line-text"> `+s[i].likeCount+` </p>

                        </div>

                        <div class="third-line-description-dislikes">

                            <img class="third-line-image-4" src=` + dislikes_url + `>

                            <p class="third-line-text"> `+s[i].dislikeCount+` </p>

                        </div>

                    </div>

  
                  </div>
  
              </div>

              </a>
  
              <br>
  
          </div>`;

      }

      else if (i==number_of_search_results-1){

        box.innerHTML =` 
      
        <div class="main-container" style="border-bottom: solid 1px black;border-right: solid 1px black;
                                           border-left: solid 1px black;border-radius: 0px 0px 10px 10px;
                                           margin-top:` + (275+20+239*(i)) + `px;
                                           position: absolute;
                                           left:50%;
                                           margin-left:-500px;">
  
              <br>

              <a href="/video/`+ids[i]+`">

  
              <div class="search-container" style="margin-bottom:20px;">
  
                  <div class="search-thumbnail">
  
                      <img class="search-thumbnail-image" src=` + th[i] + `>
  
                  </div>
  
                  <div class="search-description">
  
                      <div class="search-description-title">
                          
                          <p class="search-description-title-text">`+ti[i]+`</p>
  
                      </div>
  
                      <div class="search-description-channel">
  
                          <div class="search-description-channel-left">
  
                              <p class="search-description-channel-left-text">` + ct[i] + ` &#183; Upload Date : `+p[i]+` </p>
  
                          </div>
  
                          <div class="search-description-channel-right">
  
                              <img class="search-description-channel-right-image" src=` + views_url + `>
  
                              <p class="search-description-channel-right-text"> &#183; `+vc[i]+` Views</p>
  
                          </div>
  
                      </div>
  
                    <div class="third-line-description">

                        <div class="third-line-description-favorite">

                            <img class="third-line-image-2" src=` + favorites_url + `>

                            <p class="third-line-text">`+s[i].favoriteCount+` </p>

                        </div>

                        <div class="third-line-description-likes">

                            <img class="third-line-image-3" src=` + likes_url + `>

                            <p class="third-line-text"> `+s[i].likeCount+` </p>

                        </div>

                        <div class="third-line-description-dislikes">

                            <img class="third-line-image-4" src=` + dislikes_url + `>

                            <p class="third-line-text"> `+s[i].dislikeCount+` </p>

                        </div>

                    </div>

  
                  </div>
  
              </div>

              </a>
  
              <br>
  
          </div>
          
          <div class="break" style="height:100px;width:100px;margin-bottom:100px;
                                    margin-top:` + (275+20+239*(i+1)) + `px;
                                    position: absolute;
                                    left:50%;
                                    margin-left:-500px;">
          </div>`;

      }

      else{

        box.innerHTML =` 
      
        <div class="main-container" style="border-right: solid 1px black;border-left: solid 1px black;
                                           margin-top:` + (275+20+239*(i)) + `px;
                                           position: absolute;
                                           left:50%;
                                           margin-left:-500px;">
  
              <br>

              <a href="/video/`+ids[i]+`">

  
              <div class="search-container">
  
                  <div class="search-thumbnail">
                  
                      <img class="search-thumbnail-image" src=` + th[i] + `>
  
                  </div>
  
                  <div class="search-description">
  
                      <div class="search-description-title">
                          
                          <p class="search-description-title-text">`+ti[i]+`</p>
  
                      </div>
  
                      <div class="search-description-channel">
  
                          <div class="search-description-channel-left">
  
                              <p class="search-description-channel-left-text">` + ct[i] + ` &#183; Upload Date : `+p[i]+` </p>
  
                          </div>
  
                          <div class="search-description-channel-right">
  
                              <img class="search-description-channel-right-image" src=` + views_url + `>
  
                              <p class="search-description-channel-right-text"> &#183; `+vc[i]+` Views</p>
  
                          </div>
  
                      </div>
  
                    <div class="third-line-description">

                        <div class="third-line-description-favorite">

                            <img class="third-line-image-2" src=` + favorites_url + `>

                            <p class="third-line-text">`+s[i].favoriteCount+` </p>

                        </div>

                        <div class="third-line-description-likes">

                            <img class="third-line-image-3" src=` + likes_url + `>

                            <p class="third-line-text"> `+s[i].likeCount+` </p>

                        </div>

                        <div class="third-line-description-dislikes">

                            <img class="third-line-image-4" src=` + dislikes_url + `>

                            <p class="third-line-text"> `+s[i].dislikeCount+` </p>

                        </div>

                    </div>

  
                  </div>
  
              </div>

              </a>
  
              <br>
  
          </div>`;

      }

      document.body.appendChild(box);

    }

  }
