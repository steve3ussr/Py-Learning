# Quick Start

我想在html页面上显示两个按钮：

```html
<button onclick="window.alert('fuck TP')">click me pls. </button><br>
<button onclick="window.confirm('are you sure to leave?')">click me pls. </button>
```

可以把点击后的动作写在js文件里：

```js
function pop_alert(str) {
    window.alert('Hello, world! ' + str)}
function pop_confirm(str) {
    window.confirm(str)}
```

同时需要在html引入js文件，并且调用函数：

```html
<script src="C:\Archive\Repository\Python-Learning\selenium\example_window_alert\click_to_pop.js"></script>
<button onclick="pop_alert('fuck TP')">click me pls, i can pop an alert. </button><br>
<button onclick="pop_confirm('Are you sure to leave TP-LINK? ')">click me pls, i can pop a confirm. </button>
```



# DOM

> Document Object Model

![](https://www.w3schools.com/whatis/img_htmltree.gif)

- browser create tree structure for every web page
- each HTML element is an object
- an object has: properties, methods, events
- JS can add/remove/modify property/method/event
- JS can react to events



Shadow DOM: a DOM inside an element. Main DOM and shadow DOM are isolated. 

![](https://pic4.zhimg.com/v2-f67437f4810aa6a957ea31f47dfe28e1_1440w.jpg)

