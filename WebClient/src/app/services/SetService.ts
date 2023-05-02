import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { DTOSet } from '../model/DTOSet';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class SetService {

   
  private readonly SETS_API_URL = 'http://localhost:8000/collection/sets';
  private setsSampleUrl = 'assets/sample/sets.json';
  constructor(private http: HttpClient) { }

  getSets() {
    return this.http.get<DTOSet[]>(this.setsSampleUrl);
  }

  deleteSet(id: number): Observable<any> {
    return this.http.delete<any>(`${this.SETS_API_URL}/${id}`);
  }
}