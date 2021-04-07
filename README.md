# Sliding Puzzle Bot using A<sup>*<sup>

### The Webapp is deployed on heroku, <a href="https://sliding-puzzle-kartik33.herokuapp.com/guest">link to the guest API endpoint</a>.

Backend webapp application to solve 3X3 <a href="https://en.wikipedia.org/wiki/Sliding_puzzle">sliding tile puzzle</a>.

Input: [0 - 8] where 0 is the empty tile. eg: "0,1,2,3,4,5,6,7,8"

Output: Optimal number of moves to reach the goal state.

Features:

<ul>
  <li>RESTFul API
    <ul>
      <li>Statless authentication using <a href="https://auth0.com">auth0</a> (JWT)</li>
      <li>Uniform interface</li>
      <li>Client-Server</a>
    </ul>
  </li>
  <li>Database connectivity to save user profile and board state tried by him/her.</li>
  <li>Role-based design pattern to grant permissions to user/admin.</li>
</ul>

<table>
  <tr>
    <th>Roles</td>
    <td>admin</th>
    <td>player</td>
  </tr>
  <tr>
    <td>Permissions</td>
      <td>
        <ol>
          <li>delete:player</li> 
          <li>get:player</li>  
          <li>insert:dummy (For testing)</li> 
          <li>delete:dummy (For testing)</li>
        </ol>
    </td>
    <td>
      <ol>
        <li>get:board</li> 
        <li>delete:board</li> 
        <li>patch:board</li> 
        <li>post:solve_puzzle</li>
      </ol>
     </td>
  </tr>
  <tr>
  </tr>
</table>    

**API Documentation**
----

* **[Player](player.md)**

* **[Admin](admin.md)**

* **[Guest](guest.md)**

* **[Authentication](auth.md)**

* **[Error Formar](error.md)**
