import { Component } from '@angular/core';
import { FormControl, FormGroup } from '@angular/forms';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent {
  loginForm: FormGroup;

  ngOnInit() {
    this.loginForm = new FormGroup({
      'name': new FormControl("Nazwa użytkownika"),
      'email': new FormControl(null),
      'password': new FormControl(null),
      'confirm_password': new FormControl(null)
    }
    );
  }
  onSubmit() {
    console.log(this.loginForm);
  }

}




