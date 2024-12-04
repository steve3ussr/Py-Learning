# TODO

- [x] WebdriverWait
- [ ] Wait for the new tab to finish loading content
- [ ] from selenium.webdriver.support import expected_conditions as EC
- [ ] execute scripts
- [x] cookie, add
- [x] css selector
- [x] xpath向前向后查找, 可以通过子元素定位父元素
- [ ] actions
- [ ] headless



# Selenium的核心: Webdriver

> [reference](https://www.selenium.dev/documentation/webdriver)
>
> Selenium 通过使用*WebDriver*支持市场上所有主流浏览器的自动化。WebDriver 是一种 API 和协议，它定义了一个与语言无关的接口来控制 Web 浏览器的行为。每个浏览器都由特定的 WebDriver 实现支持，称为*驱动程序*。驱动程序是负责委托给浏览器的组件，并处理与 Selenium 和浏览器之间的通信。
>
> 这种分离是为了让浏览器供应商负责其浏览器的实现而做出的有意识的努力的一部分。Selenium 尽可能使用这些第三方驱动程序，但也提供由项目维护的自己的驱动程序，以应对无法实现的情况。



# Initiate and Quit Webdriver

使用webdriver很简单, 只需要:

```python
from selenium import webdriver

driver = webdriver.Chrome()
```



---



```python
# common scripts
try:
    driver.statements
except EC:
    do something
finally:
    driver.quit()
    
    
# test framework
def tearDown(self):
    self.driver.quit()
```

> Quit will:
> - Close all the windows and tabs associated with that WebDriver session
> - Close the browser process
> - **Close the background driver process**
> - Notify Selenium Grid that the browser is no longer in use so it can be used by another session (if you are using Selenium Grid)
>
> **Failure to call quit will leave extra background processes and ports running on your machine** which could cause you problems later.
>
> Some test frameworks offer methods and annotations which you can hook into to tear down at the end of a test.

# Browser Interaction & Info

## Navigation

- `driver.get(url)`
- `driver.refresh(), forward(), back()`





## Info

- `driver.title`
- `driver.current_url`

# Window and Tab

## 创建新tab/window , 并且切换过去

- `driver.switch_to.new_window('tab')`(开一个新标签页)
- `driver.switch_to.new_window('window')(开一个新窗口)`

## 获得tab的句柄

- 当前的`driver.current_window_handle`
- 所有的`driver.window_handle`, 返回array; 顺序为tab创建的顺序
- `driver.switch_to.window([window_handle])`可以切换过去

## 关闭tab

`driver.close()`, 注意此时webdriver focus的仍然是不存在的, 刚刚关闭的这个tab; 因此在close之后再想get url或者其他操作都是不可能的; 建议在close之后switch to另一个window

> Forgetting to switch back to another window handle after closing a window will leave WebDriver executing on the now closed page, and will trigger a **No Such Window Exception**. You must switch back to a valid window handle in order to continue execution.

```python
driver.close()
driver.switch_to.window(driver.window_handles[-1])
```



## Window size

- `driver.get_window_size()` return a dict: `{'width': 100, 'height': 100}`
- `driver.set_window_size(width, height)`



## Window Position and Size

- `driver.get_window_position()` return a dict: `{'width': 100, 'height': 100}`
- `driver.set_window_position(0, 0)`会把window放在左上角
- `driver.maximize/minimize/fullscreen_window()`



# Screenshot and Print

- `driver.save_screenshot(dir)`
- `element.screenshot(dir)`



print is only available in Chrome headless mode. 

```python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument('--headless=new')
driver = webdriver.Chrome(CHROMEDRIVER_PATH, options=options)
```



# Web Element Info

- is_displayed()
- is_enabled()
- is_selected()
- tag_name
- rect -> (x, y, height, width), coord of top left corner
- value_of_css_property(‘[key_name]’)
- text
- get_attrivute(key)
- 

# Find element

> - `from selenium.webdriver.common.by import By`
> - `find_element()返回第一个匹配到的元素，否则报错`
> - `find_elements()返回所有匹配元素的列表`
> - `driver.switch_to.active_element`可以返回当前获得focus的元素



## DOM

- `driver.fine_element()`默认从整个DOM开始匹配
- 在一整个DOM中匹配很慢，因此可以缩小匹配范围，如：`sub = driver.find(), element = sub.find()`
- 在driver中可找到shadow host, 其shadow root类似于driver，是一个DOM的父节点；之后只能在shadow root下查找元素





## Strategies to Locate

- [x] ID
- [x] XPATH
- [x] LINK_TEXT (only work with `<a>`)
- [x] PARTIAL_LINK_TEXT
- [x] NAME
- [x] TAG_NAME
- [x] CLASS_NAME
- [x] CSS_SELECTOR
- [ ] *by JS*





## Special Cases

- 不可见：`<div style='display:none'>`
- 隐藏：hidden
- 不可用，灰色：disabled
- 不可编辑：readonly
- frame/iframe
- 一样的元素



## Xpath

绝对路径, 以`/`开头

- 从第一个标签开始匹配, 例如`/html/body/div[1]/div[2]`
- 缺点: 可扩展性差, 如果中途某一个标签没找到就会失败
- 使用频率: 基本不用



相对路径, 以`//`开头

- 从某一个特定的标签开始匹配, 例如`//input`
- 可以用相对路径+属性定位，如`//input[@id="app"]`，指的是input这个标签下，属性为id，值为app的元素
- 属性可以组合，如`[@id="app" and @name="qq"]`。and，or都可以
- 通配符*，如`//*[@*="app" and @*="qq"]`，匹配任意标签/属性key，但属性value是不能用通配符的
- 更多的属性值定位方式：

  - `[starts-with(@id, "ap")]`
  - `[substring(@id, 2)="pp")]`，从第2个字符开始，后面的字符串等于pp

  - `[contains(@id, "p")]`，只要包含p这个子字符串就行
- 通过文本定位

  - `//input[text()="something"]`
  - 可以和以上组合，如`//input[contains(text(), "something)"]`
- 相对路径可以嵌套, 例如`//div[@id='app']//input`；如果从整个DOM根节点开始匹配，那就只使用`//`；如果以某个元素作为父节点开始匹配，需要`.//`；

---

XPath可以实现向前向后查找。前面的主要都是通过父元素/DOM根节点查找某个子元素，也可以通过子元素查找父元素。

XPath中`.`代表元素自己，`..`代表上一级，因此可以这样定位父元素：

```python
child = driver.find_element(By.XPATH, r'//input[@id="kw"]')
parent = chiled.find_element(By.XPATH, r'./..')
grandparent = chiled.find_element(By.XPATH, r'./../..')
```

或者这样:

```
grandparent = chiled.find_element(By.XPATH, r'./parent::*/parent::*')
```

还可以查找兄弟:

```python
input_button = input_field.find_element(By.XPATH, r'./parent::*/following::*[contains(@class, "btn")]//input[@type="submit"]')
```









## CSS selector

> 使用CSS Selector定位元素, 比XPATH更快更准确也更容易, 是Selenium官方推荐的方法.

特点:

- 不支持XPATH的相对套相对, 只能支持先相对然后再绝对;
- 简写, `#app`相当于`[@id="app"]`, `.app`相当于`[@class="app"]`
- 和XPATH一样支持更多属性: `[id="app"]`
- 用`>`代替XPATH中的`/`



## class name, name, id

根据元素本身的属性值来定位, 例如: 

```python
driver.find_element(By.ID, "username")
```



## tag name

通过HTML标签来定位, 例如寻找超链接:

```python
driver.find_element(By.TAG_NAME, "a")
```

## (partial) link text

locate link text. 

## JS

可以通过JS获取父元素: 

```python
parent_element = driver.execute_script("return arguments[0].parentElement;", child_element)
```



# Browser Popup: Alert, Confirm, Prompt

- `driver.switch_to.alert`可用于定位alert dialog
- 浏览器中同一时间只能存在一个alert dialog
- alert dialog只能显示文字，并且还有按钮
- 生成alert dialog的方法: 
  - `window.alert`: 只有一个accept
  - `window.confirm`: 可以accept, dismiss
  - `window.prompt`: accept, dismiss, send_keys (用于填写内容)

# Interact with Web Element (High-Level)

## How to Click?

- `element.click()`
- `driver.execute_script('arguments[0].click();', element)`

Selenium 的 `click()` 方法依赖浏览器的原生点击事件模拟，并会检查以下条件：

- **元素可见性**：元素必须是可见的且未被覆盖，否则会抛出异常，如 `ElementNotInteractableException` 或 `ElementClickInterceptedException`。
- **元素的可点击区域**：点击的坐标必须落在元素的边界内，如果有 `padding` 或透明区域，也可能导致问题。
- **页面加载或动态变化**：如果页面加载未完成，或元素在点击时位置发生变化（例如动画效果），可能会导致点击失败。

`execute_script('arguments[0].click();', element)` 通过 JavaScript 直接触发元素的 `click` 事件，而不依赖于 Selenium 对浏览器的原生模拟，因此它可以绕过某些限制：

- **元素可见性**：即使元素不可见或被遮挡，JavaScript 仍然可以触发点击事件。
- **动态变化**：不受动画、样式等变化影响，因为它不需要实际模拟鼠标的点击行为。
- **复杂结构的元素**：对于某些复杂的 HTML 结构（例如带有自定义事件的按钮），JavaScript 能更可靠地触发绑定的事件。



## FileUpload

不能和操作系统的FileManager交互，只能先找到输入框，send file path。

```python
    file_input = driver.find_element(By.CSS_SELECTOR, "input[type='file']")
    file_input.send_keys(upload_file)
    driver.find_element(By.ID, "file-submit").click()
```





## Execute script

```python
    # Stores the header element
header = driver.find_element(By.CSS_SELECTOR, "h1")

    # Executing JavaScript to capture innerText of header element
driver.execute_script('return arguments[0].innerText', header)
```



## send keys

通常可以对文本框使用`send_keys()`方法. 如果该元素不可编辑, 会报错. 

## clear

要求元素可编辑, 并且可以被重置. 

`WebElement.clear()`

## List Options



```python
select = Select(select_element)
select.options # get all options
select.all_selected_options # get all selected options

# select methods
select.select_by_visible_text('Four')
select.select_by_value('two')
select.select_by_index(3)

# deselect
select.deselect_by_value('eggs')
```



# Interact with Web Element (Low-Level)

> simulate device input:
>
> - key
> - pointer
> - wheel









# Cookies



通过`driver.add_cookie(cookie_dict)`可添加cookie,但要注意:

- cookie只能对cookie有效的域使用, 例如taobao的cookie不能用于bilibili
- cookie
- 如果准备在与网站交互之前预设 Cookie，并且您的主页很大/需要一段时间才能加载，则替代方法是在网站上找到较小的页面（通常 404 页面较小，例如http://example.com/some404page）
- 添加 Cookie 仅接受一组定义的可序列化的 JSON 对象。[以下](https://www.w3.org/TR/webdriver1/#cookies)是接受的 JSON 键值列表的链接





# Frame and iFrame

> **iFrame** 是 **HTML** 的一个标签，代表 **inline frame**，用于在网页中嵌入另一个 HTML 页面。通过 iFrame，你可以在一个网页中显示另一个独立网页的内容，就像一个“网页中的小窗口”。

如果一个页面中嵌套了多个其他页面，selenium默认只会搜索最顶层的frame; 如果要定位某个iframe中的元素, 需要首先切换至相应的iframe.

切换iframe的方式和切换窗口差不多: 

- 首先定位iframe`iframe = driver.fine_element(By.ID, 'id')`
- `driver.switch_to.frame(iframe)`
- 退出iframe: `driver.switch_to.default_content`



# Wait!

浏览器自动化最常见的挑战可能是确保 Web 应用程序处于按预期执行特定 Selenium 命令的状态。这些过程通常会陷入竞争状态，有时浏览器首先进入正确状态（一切按预期工作），有时 Selenium 代码首先执行（一切未按预期工作）。这是不稳定测试的主要原因之一。

所有导航命令都会根据页面加载策略等待`readystate`变量的特定值（通常为`complete`），然后driver才会将控制权还给代码。`readyState`仅与加载 HTML 中定义的资产有关，但加载的 JavaScript 资产通常会导致网站发生变化，并且当代码准备好执行下一个 Selenium 命令时，需要交互的元素可能尚未出现在页面上。

同样，在很多单页应用程序中，元素会动态添加到页面中或根据点击更改可见性。元素必须同时存在并 [显示](https://www.selenium.dev/documentation/webdriver/elements/information/#is-displayed)在页面上，Selenium 才能与其交互。

有几种可用的等待方法：

## time.sleep



许多人想到的第一个解决方案是添加一个 sleep 语句，以暂停代码执行一段时间。由于代码无法确切知道需要等待多长时间，因此当代码的休眠时间不够长时，此方法可能会失败。或者，如果值设置得太高，并且在每个需要的地方都添加了 sleep 语句，则会话的持续时间可能会变得过长。

Selenium 提供了两种不同的、更好的同步机制。

## implicit_wait

`driver.implicit_wait(2)`

这是一个全局设置，适用于整个会话的每个元素定位调用。默认值为`0`，这意味着如果未找到元素，它将立即返回错误。如果设置了隐式等待，驱动程序将等待所提供值的持续时间，然后再返回错误。请注意，一旦找到元素，驱动程序将返回元素引用，代码将继续执行，因此更大的隐式等待值不一定会增加会话的持续时间。

*警告：* 不要混合使用隐式和显式等待。这样做可能会导致不可预测的等待时间。例如，设置 10 秒的隐式等待和 15 秒的显式等待可能会导致 20 秒后发生超时。



## explicit_wait

*显式等待*是添加到代码中的循环，在退出循环并继续执行代码中的下一个命令之前，它会轮询应用程序是否有特定条件被评估为真。如果在指定的超时值之前条件未得到满足，代码将给出超时错误。由于应用程序有多种方式无法处于所需状态，因此显式等待是指定每个需要等待的确切条件的绝佳选择。另一个不错的功能是，默认情况下，Selenium Wait 类会自动等待指定元素的存在。

```
wait = WebDriverWait(driver, timeout=2)
wait.until(lambda d: some_element.is_displayed())
```

WeDriverWait对象可以自定义，包括：

- 更改代码评估频率（轮询间隔）
- 指定应自动处理哪些异常
- 更改总超时长度
- 自定义超时消息

```python
errors = [NoSuchElementException, ElementNotInteractableException]
    wait = WebDriverWait(driver, timeout=2, poll_frequency=.2, ignored_exceptions=errors)
    wait.until(lambda d : revealed.send_keys("Displayed") or True)
```

