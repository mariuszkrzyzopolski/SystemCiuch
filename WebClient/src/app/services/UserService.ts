import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class UserService {
  private readonly baseUrl = 'http://localhost:8000/user';

  constructor(private http: HttpClient) {}

  public removeUser(): Observable<void> {
    return this.http.delete<void>(`${this.baseUrl}`);
  }

  updateUser(body: any): Observable<void> {
    return this.http.patch<void>(`${this.baseUrl}`, body);
  }
}