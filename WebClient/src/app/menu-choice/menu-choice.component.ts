import { Component, Input} from '@angular/core';

@Component({
  selector: 'app-menu-choice',
  templateUrl: './menu-choice.component.html',
  styleUrls: ['./menu-choice.component.css']
})

export class MenuChoiceComponent {
  @Input() name = '';
  @Input() route ='';
}
