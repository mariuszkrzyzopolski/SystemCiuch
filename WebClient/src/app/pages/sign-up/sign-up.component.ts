import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup } from '@angular/forms';

@Component({
  selector: 'sign-up.component',
  templateUrl: './sign-up.component.html',
  styleUrls: ['./sign-up.component.css']
})
export class SignUpComponent implements OnInit {
  signupForm: FormGroup;

  ngOnInit() {
    this.signupForm = new FormGroup({
      'name': new FormControl("Nazwa użytkownika"),
      'email': new FormControl(null),
      'password': new FormControl(null),
      'confirm_password': new FormControl(null)
    }
    );
  }
  onSubmit() {
    console.log(this.signupForm);
  }

}

