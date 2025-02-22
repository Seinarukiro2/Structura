/*
  Warnings:

  - A unique constraint covering the columns `[uid]` on the table `Payment` will be added. If there are existing duplicate values, this will fail.
  - Added the required column `uid` to the `Payment` table without a default value. This is not possible if the table is not empty.

*/
-- AlterTable
ALTER TABLE "Payment" ADD COLUMN     "uid" TEXT NOT NULL;

-- CreateIndex
CREATE UNIQUE INDEX "Payment_uid_key" ON "Payment"("uid");
