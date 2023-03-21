import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { SignUp } from '../../model/SignUp';

@Component({
  selector: 'sign-up.component',
  templateUrl: './sign-up.component.html',
  styleUrls: ['./sign-up.component.css']
})


export class SignUpComponent implements OnInit {
  signUpForm: FormGroup;
  loginForm: FormGroup;
  constructor(private http: HttpClient) { }

  ngOnInit() {
    this.signUpForm = new FormGroup({
      'mail': new FormControl(null, [Validators.required, Validators.email]),
      'city': new FormControl(null, [Validators.required]),
      'password': new FormControl(null, [Validators.required, Validators.minLength(6)]),
      'repeated_password': new FormControl(null, [Validators.required, Validators.minLength(6)]),
    }
    );
  }

  onSubmit() {
    this.submitForm(this.signUpForm.value);
  }

  submitForm(signUp: SignUp) {
    this.http.post('http://127.0.0.1:8000/user/register', signUp).subscribe(
      (response: any) => console.log(response.token),
      (error) => console.log(error.error.detail)
    )
  }
}

