import { HttpClient, HttpParams } from '@angular/common/http';
import {  Injectable } from '@angular/core';
import * as moment from "moment";
import {env} from "../app.component";



@Injectable({
  providedIn: 'root',
})
export class AuthService {
  constructor(private http: HttpClient) {
  }

  login(email: string, password: string) {
    return this.http.post<User>(env.url+'/user/login', {mail: email, password})
  }
  
  public setSession(authResult:any) {
    
    const expiresAt = moment().add(authResult.expiresIn, 'second');

    localStorage.setItem('id_token', authResult.token);
    localStorage.setItem("expires_at", JSON.stringify(expiresAt.valueOf()));
  }

  logout() {
    localStorage.removeItem("id_token");
    localStorage.removeItem("expires_at");
  }

  public isLoggedIn() {
    return localStorage.getItem('id_token');
  }

  isLoggedOut() {
    return !this.isLoggedIn();
  }

  getExpiration() {
    const expiration: string | null = localStorage.getItem("expires_at");
    const expiresAt = JSON.parse(expiration!);
    return moment(expiresAt);
  }
}

interface User {
  email: string,
  password: string 
}