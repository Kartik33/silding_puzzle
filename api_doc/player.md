***Header***

**`-H "Authorization: Bearer ${jwt} ${id_token}"`**
----
  * ***NOTE: The space between "Bearer", jwt and it_token is necessary***
  * Look in authentication document to obtains jwt and id_token.


**`/player/<int:player_id>/boards`**
----

Returns the list of boards for this player

* **Method:** `GET`

* **Success Response:**
  * **Code:** 200 <br />
    **Content:** `{ boards : [ {board_id:12, board_state: "0,1,2,3,4,5,6,7,8"}], {.....}, {......} }`
    
    
    
**`/board/<int:board_id>`**
----

Delete the board from the database

* **Method:** `DELETE` | `PATCH`

* **Success Response:**
  * **Code:** 200 <br />
    **Content:** `{ board_id: 12}`
    
    
    
**`/solve`**
----

Saves the optimal moves and returns the optimal moves

* **Method:** `POST'

* **Data Params** 

* **Success Response:**
  * **Code:** 200 <br />
    **Content:** `{ board_state: board_state, moves="[Move-right, Move-up,...]",user_id:12}`
    
    
**[Error Format](error.md)**
    
    
