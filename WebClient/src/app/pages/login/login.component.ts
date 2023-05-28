import { Component } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from 'src/app/authService/auth-service.component';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent {
  loginForm: FormGroup;
  loginFail: boolean;

  constructor(
    private authService: AuthService,
    private router: Router) {

    this.loginForm = new FormGroup({
      'email': new FormControl(null, [Validators.required, Validators.email]),
      'password': new FormControl(null, [Validators.required, Validators.minLength(6)]),

    }
    );
  }

  ngOnInit() {

  }

  onSubmit() {
    const val = this.loginForm.value;

    if (val.email && val.password) {
      this.authService.login(val.email, val.password)
        .subscribe(
          (result) => {
            this.authService.setSession(result);
            this.router.navigateByUrl('/');
            this.loginFail = false;
          },
          (error) => {
            this.loginFail = true;
          }
        );
    }
  }

  close() {
    this.loginFail = false;
  }

  onRegister() {
    this.router.navigate([ '/sign-up' ])
  }
  
}




