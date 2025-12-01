import {UserRepository } from '../repositories/user.repository.js'


export class UserService {
  static async createUser(payload) {
    return await UserRepository.create(payload);
  }
}