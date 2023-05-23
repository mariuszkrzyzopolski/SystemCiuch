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

  goToAutomaticCreateSet() {
    this.router.navigate([ '/automatic-create-set' ])
  }

  goToManualCreateSet() {
    this.router.navigate([ '/manual-create-set' ])
  }
}