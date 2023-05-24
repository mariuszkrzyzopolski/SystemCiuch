import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';
import { Router } from '@angular/router';
import { UserService } from 'src/app/services/UserService';

@Component({
  selector: 'app-settings',
  templateUrl: './settings.component.html',
  styleUrls: ['./settings.component.css']
})
export class SettingsComponent implements OnInit {
showRemoveModal = false;
showUpdateModal = false;
userForm: FormGroup;

constructor(private userService: UserService, private router: Router, private fb: FormBuilder) {}

ngOnInit(): void {
  this.userForm = this.fb.group({
    email: [''],
    password: [''],
    city: ['']
  });
}


updateUser(): void {
  const { email, password, city } = this.userForm.value;
  const user = { mail: email, password, city };
  this.userService.updateUser(user).subscribe(
    (response) => {
      this.showUpdateModal = true;
    }
  );
}

remove(): void {
  this.userService.removeUser().subscribe(
    (response) => {
      // Handle success response
      this.router.navigate(['/login']);
    }
  );
}
}
