import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';

@Component({
  selector: 'sign-up.component',
  templateUrl: './sign-up.component.html',
  styleUrls: ['./sign-up.component.css']
})
export class SignUpComponent implements OnInit {
  signUpForm: FormGroup;

  ngOnInit() {
    this.signUpForm = new FormGroup({
      'email': new FormControl(null,[Validators.required, Validators.email]),
      'city': new FormControl(null,[Validators.required]),
      'password': new FormControl(null, [Validators.required, Validators.minLength(6)]),
      'confirm_password': new FormControl(null, [Validators.required, Validators.minLength(6)])
    }
    );
  }
  onSubmit() {
    console.log(this.signUpForm.value);
  }
  }



