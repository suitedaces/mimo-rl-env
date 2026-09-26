NavigationBarLabelBehavior not working
Navigation bar labels options not working on android or web using the following code:

```
def main(page: ft.Page):
    page.title = "Badge on a NavigationBar destination icon"
    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationDestination(
                icon_content=ft.Badge(
                    content=ft.Icon(ft.icons.EXPLORE),
                    small_size=10,
                ),
                label="Explore",
            ),
            ft.NavigationDestination(icon=ft.icons.COMMUTE, label="Commute"),
            ft.NavigationDestination(
                icon_content=ft.Badge(content=ft.Icon(ft.icons.PHONE), text="8")
            ),
        ],
        label_behavior=ft.NavigationBarLabelBehavior.ALWAYS_HIDE
    )
    page.add(ft.Text("Body!"))


ft.app(target=main)
```
Labels are not hidden when using option ft.NavigationBarLabelBehavior.ALWAYS_HIDE

![image](https://github.com/flet-dev/flet/assets/29530317/10e1d848-8618-4e5e-bc9f-265baee6262f)
