"""
마이크 테스트 스크립트
"""
import speech_recognition as sr

def test_microphone():
    print("=" * 50)
    print("마이크 진단 테스트")
    print("=" * 50)
    print()

    # 1. 사용 가능한 마이크 나열
    print("1. 사용 가능한 마이크 목록:")
    print("-" * 50)
    for index, name in enumerate(sr.Microphone.list_microphone_names()):
        print(f"  [{index}] {name}")
    print()

    # 2. 기본 마이크 테스트
    print("2. 기본 마이크 초기화 테스트:")
    print("-" * 50)
    try:
        recognizer = sr.Recognizer()
        mic = sr.Microphone()
        print("✅ 마이크 초기화 성공")

        # 3. 주변 소음 측정
        print()
        print("3. 주변 소음 레벨 측정 (2초):")
        print("-" * 50)
        with mic as source:
            print("측정 중...")
            recognizer.adjust_for_ambient_noise(source, duration=2)
            print(f"✅ 에너지 임계값: {recognizer.energy_threshold}")
            print(f"   동적 에너지: {recognizer.dynamic_energy_threshold}")

        # 4. 짧은 오디오 캡처 테스트
        print()
        print("4. 오디오 캡처 테스트 (5초):")
        print("-" * 50)
        print("⚠️  지금 말해보세요: '테스트'")
        print()

        with mic as source:
            try:
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                print("✅ 오디오 캡처 성공!")

                # Google API 테스트
                print()
                print("5. Google Speech API 테스트:")
                print("-" * 50)
                try:
                    text = recognizer.recognize_google(audio, language="ko-KR")
                    print(f"✅ 인식 성공: '{text}'")
                except sr.UnknownValueError:
                    print("⚠️  음성을 인식하지 못했습니다")
                    print("   - 말을 하셨나요?")
                    print("   - 소리가 충분히 컸나요?")
                except sr.RequestError as e:
                    print(f"❌ API 오류: {e}")

            except sr.WaitTimeoutError:
                print("⚠️  타임아웃: 소리가 감지되지 않았습니다")
                print("   - 마이크가 음소거되어 있지 않나요?")
                print("   - 마이크 권한이 허용되어 있나요?")

    except Exception as e:
        print(f"❌ 마이크 초기화 실패: {e}")
        print()
        print("해결 방법:")
        print("  - 시스템 설정 → 개인정보 보호 → 마이크 권한 확인")
        print("  - 마이크가 제대로 연결되어 있는지 확인")
        return

    print()
    print("=" * 50)
    print("진단 완료")
    print("=" * 50)

if __name__ == "__main__":
    test_microphone()
