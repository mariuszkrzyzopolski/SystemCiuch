import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-create-set',
  templateUrl: './create-set.component.html',
  styleUrls: ['./create-set.component.css']
})
export class CreateSetComponent {
  constructor(

    private router: Router) {
  }

  goToManualCreateSet() {

    this.router.navigate([ '/manual-create-set' ])
  }
}