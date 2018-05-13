class SubmissionStatus(object):
    PENDING = 0
    AC = 1
    WA = 2
    CE = 3
    TLE = 4
    MLE = 5
    PE = 6
    SE = 7


SUBMISSION_STATUS_CHOICE = (
    (SubmissionStatus.PENDING, 'Pending'),
    (SubmissionStatus.AC, 'Accepted'),
    (SubmissionStatus.WA, 'Wrong Answer'),
    (SubmissionStatus.CE, 'Compile Error'),
    (SubmissionStatus.TLE, 'Time Limit Exceed'),
    (SubmissionStatus.MLE, 'Memory Limit Exceed'),
    (SubmissionStatus.PE, 'Presentation Error'),
    (SubmissionStatus.SE, 'System Error'),
)
