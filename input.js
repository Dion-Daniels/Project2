var request = new XMLHttpRequest()

request.open('GET', 'INSERT API LINK HTML HERE', true)
request.onload = function () {
  // Begin accessing JSON data here
  var data = JSON.parse(this.response)

  if (request.status >= 200 && request.status < 400) {
    data.forEach(player) => {
      console.log(games_by_players.player_tag)
    })
  } else {
    console.log('error')
  }
}

request.send()