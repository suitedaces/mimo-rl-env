<!-- ✨ Thanks for reporting a bug! ➡️ Please don't ignore this template -->

<!-- 1️⃣ Explain here what's wrong -->

The above rule reports errors for class properties that match the rule.

<!-- 2️⃣ Specify which rule is buggy here and in the title -->

<!-- 3️⃣ Add some examples where the issue appears -->

```ts
@Component({
  selector: 'app-headline',
  templateUrl: './headline.component.html',
  styleUrls: ['./headline.component.scss'],
})
export class HeadlineComponent implements OnInit {
  @Input() size?: HeadlineSizes

  ngOnInit(): void {
    if (this.size) this.classes.push(this.size) // ← reported
  }
}
```
