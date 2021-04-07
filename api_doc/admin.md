***Header***

**`-H "Authorization: Bearer ${jwt} ${id_token}"`**
----
  * ***NOTE: The space between "Bearer", jwt and it_token is necessary***
  * Look in authentication document to obtains jwt and id_token.


**`/player`**
----

Returns a list of players

* **Method:** `GET`

* **Success Response:**
  * **Code:** 200 <br />
    **Content:** `{ players: players}`
    
    
**`/player/<int:player_id>`**
----

Deletes the player with player_id

* **Method:** `DELETE`

* **Success Response:**
  * **Code:** 200 <br />
    **Content:** `{ player_id : 12 }`

**[Error Format](error.md)**
