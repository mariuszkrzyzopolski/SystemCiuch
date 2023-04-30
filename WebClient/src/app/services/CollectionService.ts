import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { DTOCollection } from '../model/CollectionDTO';

@Injectable({
  providedIn: 'root'
})
export class CollectionService {
  private apiUrl = 'http://localhost:8000/collection';
  private collectionUrl = 'assets/sample/collection.json';


  constructor(private http: HttpClient) { }

  getCollection(): Observable<DTOCollection> {
    return this.http.get<DTOCollection>(this.apiUrl);
  }

  deleteCollectionItem(id: number): Observable<any> {
    return this.http.delete<any>(`${this.apiUrl}/item/${id}`);
  }
}