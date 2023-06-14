import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { SignUp } from '../../model/SignUp';
import {env} from "../../app.component";

@Component({
  selector: 'sign-up.component',
  templateUrl: './sign-up.component.html',
  styleUrls: ['./sign-up.component.css']
})


export class SignUpComponent implements OnInit {
  signUpForm: FormGroup;
  loginForm: FormGroup;
  signupSuccess = false;
  signupFail = false;
  constructor(private http: HttpClient, private router: Router) { }

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

  login(){
    this.router.navigate(['/login']);
  }

  close(){
    this.signupSuccess = false;
    this.signupFail = false;
  } 

  submitForm(signUp: SignUp) {
    this.http.post(env.url+'/user/register', signUp).subscribe(
      (response: any) => {
        if(response.token) {
          this.signupSuccess = true;
        }
      },
      (error) => {
        this.signupFail = true;
      }
    )
  }
}

