import { Component, EventEmitter, Output } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from '../authService/auth-service.component';
@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.css']

})
export class HeaderComponent {

  constructor(
    public authService: AuthService,
    private router: Router) {
  }

  logout() {
    this.authService.logout();
    this.router.navigate(['/login'])
  }
}
